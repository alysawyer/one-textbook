import lmql
import json
from pathlib import Path
import argparse
from functools import partial
import os

def query(c):
    '''takes in a dict that includes lmql prompt and the ground truth answer, 
    returns list of dictionaries that include prompt, ground truth, and model output'''
    print("sending output")
    output = lmql.run_sync(c["code"], output_writer=lmql.stream("RESPONSE"))
    print("output returned as: " + output[0].variables['ANSWER'].strip())
    # TODO: better way to do this?
    return {"code":c["code"]}, {"answer":c["answer"]}, {"model_output":output[0].variables['ANSWER'].strip()}

def get_outputs(codes):
    '''passes lmql code to query, returns a list of dictionaries of all of the model's results'''
    results = []
    for c in codes:
        results.append(query(c))
    return results

def calculate_accuracy(model_output):
    '''takes in list that contains the model output, questions, and answers, returns accuracy score'''
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


# creating output base filename
info_list = parser.parse_args().second_argument.split(".")
model = "davinci"
if info_list[4] == "davinci:ft-personal:ch5txt-only-2023-06-15-04-29-57":
    model = "davinci-finetuned-ch5txt-only"
elif info_list[4] == "davinci:ft-personal:ch5txt-replacements-2023-06-15-01-18-46":
    model = "davinci-finetuned-ch5txt-replacements"
elif info_list[4] == "davinci:ft-personal:ch5txt-prompt-replacements-2023-06-17-19-29-25":
    model = "davinci-finetuned-ch5txt-qareplacements"
json_name = ".".join([info_list[0].split("/")[2], info_list[5], info_list[1], model, info_list[0].split("/")[1], info_list[2], info_list[3]])

# creating output filepaths
output_accuracy_file = "x/" + json_name + ".json"
output_response_file = "x/" +  json_name + ".raw.json"

if not os.path.exists(output_accuracy_file) or os.path.getsize(file_path) == 0: 
    # getting model output
    model_output = get_outputs(data["codes"]) 
    
    # to NOT re query -- replace above line with: 
    # with open(output_response_file, 'r') as file:
    #     model_output =  json.load(file)

    # exporting model output
    with open(output_accuracy_file, "w") as outfile:
        outfile.write(str(calculate_accuracy(model_output)))
    with open(output_response_file, "w") as outfile:
        outfile.write(json.dumps(model_output))
