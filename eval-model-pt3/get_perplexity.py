import lmql
import json
from pathlib import Path
import argparse
from functools import partial
import os
import openai

def get_perplexity(model, sentence):

    # define the completion parameters
    completion_parameters = {
        "model": model,
        "prompt": sentence,
        "max_tokens": 0,
        "logprobs": 0,
        "echo": True
    }

    # calling openai api to get completion response
    response = openai.Completion.create(**completion_parameters)

    # extracing the log probabilities 
    choices = response['choices'][0]
    token_logprobs = choices['logprobs']['token_logprobs']

    # converting into perplexity
    l = sum(token_logprobs[1:]) / len(token_logprobs[1:])
    perplexity = 2 ** (-l)

    return perplexity

def get_outputs(codes):
    '''passes lmql code to query, returns a list of dictionaries of all of the model's results'''
    results = []

    # for one set of questions in the file
    for question in codes:
        results.append(score_perplexity(question))
    
    print(results)
    return results



def score_perplexity(model_output):
    '''takes in list that contains the model output, questions, and answers, returns accuracy score'''

    # takes in question and possible questions

    #  check whcih one is max

    # if that is correct, score 1 for the question 

    # keeps the perplexity of the correct answer


    return sum(scores) / len(scores)

    scores = []
    for question in model_output:
        if question[1]["answer"] == question[2]["model_output"]:
            scores.append(1)
        else:
            scores.append(0)
    
    return sum(scores) / len(scores)


# getting json name
parser = argparse.ArgumentParser()
parser.add_argument('second_argument')
# opening json file
file_path = Path.cwd()/parser.parse_args().second_argument
with file_path.open(mode='r',encoding="utf-8") as f:
        data = json.load(f)


model = 'davinci'


# Iterate through questions
for item in data:
    question = item["question"]
    evalsentences = item["evalsentences"]
    answer = item["answer"]
    
    print("Question:", question)
    
    # Iterate through evalsentences
    result_list = []
    for sentence in evalsentences:
        # Evaluate each sentence and calculate perplexity
        perplexity = get_perplexity(model, sentence)
        
        # Create a dictionary with evaluated sentence and perplexity
        result = {
            "evalsentence": sentence,
            "perplexity": perplexity
        }
        
        # Append the result to the list
        result_list.append(result)
    
    # Update the evalsentences key with the result list
    item["evalsentences"] = result_list
    
    print("Result:", json.dumps(item, ensure_ascii=False, indent=4))
    
# Save the updated data to a JSON file
with open("output.json", "w") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)


# # creating output base filename
# info_list = parser.parse_args().second_argument.split(".")
# model = info_list[4]

# json_name = ".".join([info_list[0].split("/")[2], info_list[5], info_list[1], model, info_list[0].split("/")[1], info_list[2], info_list[3]])

# # creating output filepaths
# output_accuracy_file = "results/results-cap1to3/" + json_name + ".json"
# output_response_file = "results/results-cap1to3-raw/" +  json_name + ".raw.json"

# # only running new code 
# if not os.path.exists(output_accuracy_file) or os.path.getsize(file_path) == 0: 
#     # # getting model output
#     # model_output = get_outputs(data["codes"]) 

#     # # to NOT re query -- replace above line with: 
#     # # with open(output_response_file, 'r') as file:
#     # #     model_output =  json.load(file)

#     # # exporting model output
#     # with open(output_accuracy_file, "w") as outfile:
#     #     outfile.write(str(calculate_accuracy(model_output)))
#     # with open(output_response_file, "w") as outfile:
#     #     outfile.write(json.dumps(model_output))
