import json
import os
import sys
import random
import argparse
from unidecode import unidecode
def get_questions_and_answers(data):
    questions = []
    answers = []
    newquestions = []
    newanswers = []
    for x in range(len(data)):
        queststr = data[x]["q"]
        queststr = queststr.lstrip('0123456789')
        queststr = queststr.replace("#", "~")
        queststr = unidecode(queststr)
        #Remove if want accents all unidecode from next 3 lines
        questions.append(queststr)
        answerlist = [unidecode(answer) for answer in data[x]["a"]]
        answers.append(answerlist)
      #  print("answerlist=", answerlist)
        print("data[x]['a']=", data[x]["a"])
    return questions, answers

def lcg(seed, evalendings, answer, num_ans):
    retlist = []
    m = len(list(evalendings))
    a = 203956878356401977405765866929034577280193993314348263094772646453283062722701277632936616063144088173312372882677123879538709400158306567338328279154499698366071906766440037074217117805690872792848149112022286332144876183376326512083574821647933992961249917319836219304274280243803104015000563790123
    c = 319705304701141539155720137200974664666792526059405792539680974929469783512821793995613718943171723765238853752439032835985158829038528214925658918372196742089464683960239919950882355844766055365179937610326127675178857306260955550407044463370239890187189750909036833976197804646589380690779463976173*643808006803554439230129854961492699151386107534013432918073439524138264842370630061369715394739134090922937332590384720397133335969549256322620979036686633213903952966175107096769180017646161851573147596390153

    if m == 4:
        evalendings = list(evalendings)
        for ending in evalendings:
            if ending != answer:
                retlist.append(ending)
        return retlist, seed
    if m < 4:
        print(m)
        sys.exit()
    c = 7 
    evalendings = list(evalendings)
    m = len(evalendings)
    counter = 0
    while len(retlist) != (num_ans - 1):
        counter += 1
        newseed = (a * seed + c) % m
        print("newseed=", newseed)
        if evalendings[newseed] in retlist:
            pass
        else:
            if evalendings[newseed] != answer:
                retlist.append(evalendings[newseed])
        seed = newseed
        if counter > 100:
            print("m=", m)
            print("seed=", seed)
            c += 1
    return retlist, seed
def split_up_tilde(questions, answers):
    newquestions = []
    newanswers = []
    for z in range(len(questions)):
        if questions[z].count("~") == 1:
            newquestions.append(questions[z])
            newanswers.append(answers[z][0])
        else:
            hat = range(len(answers[z]))
            for x in hat: 
                if questions[z].count("~") == 1:
                    newanswers.append(answers[z][0])
                    newquestions.append(questions[z]) 
                else:
                    firstindex = questions[z].find("~")
                    questint = questions[z][:firstindex] + "#" + questions[z][firstindex + 1:]
                    if questint.count("~") > 0:
                        for count in range(questint.count("~")):
                            count = count + 1
       #                     print("count)=", (count))
        #                    print("answers[z]=", answers[z])
         #                   print("questint=", questint)
                            questint = questint[:questint.find("~")] + answers[z][count] + questint[questint.find("~") + 1:]
          #                  print("questint=", questint)
                        newquestions.append(questint.replace("#", "~"))
                        newanswers.append(answers[z][0])
                        questint = questions[z][:firstindex] + answers[z][0] + questions[z][firstindex + 1:]
                        questions[z] = questint
                        del answers[z][0]
                    else:
                        newquestions.append(questint.replace("#", "~"))
                        newanswers.append(answers[z][x])
                        questint = questions[z][:firstindex] + answers[z][x] + questions[z][firstindex + 1:]
    return newquestions, newanswers
#print("newquestions=", newquestions)
#print("newanswers=", newanswers)



def generate_sentences(newquestions, newanswers, num_answers, allanswers):
    evalendings = set(newanswers)
    print("len(evalendings)=", len(evalendings))
    print("evalendings=", evalendings)
    evalsentenceslist = []
    answersentencelist = []
    evalsentences = []
    seed = 2
    for x in range(len(newquestions)):
        evalsentences = []
        question = newquestions[x]
        answer = newanswers[x]
        answersentence = question.replace("~", answer)
        answersentencelist.append(answersentence)
        evalsentences.append(answersentence)
        #add rng for eval endings here
        if allanswers == "Y":
            for ending in evalendings:
                if ending != answer:
                    evalsentences.append(question.replace("~", ending))
            
        else:
            rngevalendings, seed = lcg(seed, evalendings, answer, num_answers) 
            print("question=", question)
            for ending in rngevalendings:
                print("ending=", ending)
                if ending != answer:
                    evalsentences.append(question.replace("~", ending))
        evalsentenceslist.append(evalsentences)
    return evalsentenceslist, answersentencelist, evalsentences
#    print("evalsentences=", evalsentences)


#print("evalsentences=", evalsentences)
#print("evalsentenceslist=", evalsentenceslist)
#print("answersentencelist=", answersentencelist)

def generate_dictionary(newquestions, evalsentenceslist, answersentencelist):
    retlist = []
    for x in range(len(newquestions)):
        innerdict = {}
        innerdict["question"] = newquestions[x]
        innerdict["evalsentences"] = evalsentenceslist[x]
        innerdict["answer"] = answersentencelist[x]
        retlist.append(innerdict)
    return retlist



def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', default = 'task2update/quizstyle/PENSVMA/CAPITVLVM XXV.json')
    parser.add_argument("--output_folder", default = "cats")
    parser.add_argument("--number_of_answers", default = "4")
    parser.add_argument("--allanswers", default = "N")


    args = parser.parse_args()
    file_path = args.file_name
    number_ans = int(args.number_of_answers)
    allanswers = str(args.allanswers)
    with open(file_path, 'r') as file:
        data = json.load(file)

    questions, answers = get_questions_and_answers(data)
    newquestions, newanswers = split_up_tilde(questions, answers)
    evalsentenceslist, answersentencelist, evalsentences = generate_sentences(newquestions, newanswers, number_ans, allanswers)
    retlist = generate_dictionary(newquestions, evalsentenceslist, answersentencelist)
    output_path_base = os.path.join(args.output_folder, os.path.basename(args.file_name))
    output_path = output_path_base.replace(" ", "_")[:-5] +  ".json"

    with open(output_path, "w") as outfile:
        json.dump(retlist, outfile)




if __name__ == '__main__':
    main()
