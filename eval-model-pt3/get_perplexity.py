import json
from pathlib import Path
import argparse
from functools import partial
import os
import openai
import time

def get_perplexity(model, sentence):
    '''Queries OpenAI API to get logprobs of the prompt sentence'''

    # Define the completion parameters
    completion_parameters = {
        "model": model,
        "prompt": sentence,
        "max_tokens": 0,
        "logprobs": 0,
        "echo": True
    }

    # Check if the rate limit has been reached
    if 'last_request_time' in get_perplexity.__dict__:
        elapsed_time = time.time() - get_perplexity.last_request_time
        time_to_wait = max(0, 60 - elapsed_time)
        time.sleep(time_to_wait)

    # Calling OpenAI API to get completion response
    response = openai.Completion.create(**completion_parameters)

    # Update the last_request_time to track rate limiting
    get_perplexity.last_request_time = time.time()

    # Extract the log probabilities
    choices = response['choices'][0]
    token_logprobs = choices['logprobs']['token_logprobs']

    return token_logprobs

def evaluate_questions(questions):
    '''takes in model output json data, returns a list of 1s and 0s, where 1s represent correct answers'''
    results = []

    # iterate thru questions
    for question in questions:
        lowest_perplexity = float('inf')
        lowest_perplexity_index = -1
        for i, evalsentence in enumerate(question['evalsentences']):
            perplexity = evalsentence['perplexity']  # Extract perplexity from the evaluated sentence

            # flagging if lowest perplexity
            if perplexity < lowest_perplexity:
                lowest_perplexity = perplexity
                lowest_perplexity_index = i

        # seeing if the answer is correct, if lowest perplexity sentence is the same as the answer
        is_correct = 1 if question['evalsentences'][lowest_perplexity_index]['evalsentence'] == question['answer'] else 0
        results.append(is_correct)

    return results


# getting json name
parser = argparse.ArgumentParser()
parser.add_argument('second_argument')
# opening json file
file_path = Path.cwd() / parser.parse_args().second_argument
with file_path.open(mode='r', encoding="utf-8") as f:
    data = json.load(f)

model = "davinci"

# creating output base filename
info_list = parser.parse_args().second_argument.split(".")
json_name = ".".join([ info_list[0].split("/")[2], info_list[0].split("/")[1], model])

# creating output filepaths
output_perplexity_file = "results/full/" + json_name + ".json"
output_response_file = "results/full-raw/" +  json_name + ".raw.json"


# only running new code 
if not os.path.exists(output_response_file) or os.path.getsize(output_response_file) == 0: 
    
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
            log_probs = get_perplexity(model, sentence)

            # Calculate perplexity from log_probs
            l = sum(log_probs[1:]) / len(log_probs[1:])
            perplexity = 2 ** (-l)

            # Create a dictionary with evaluated sentence, perplexity, and log_probs
            result = {
                "evalsentence": sentence,
                "perplexity": perplexity,
                "log_probs": log_probs
            }

            # Append the result to the list
            result_list.append(result)

        # Update the evalsentences key with the result list
        item["evalsentences"] = result_list

        print("Result:", json.dumps(item, ensure_ascii=False, indent=4))

    with open(output_response_file, "w") as outfile:
        outfile.write(json.dumps(data))

    # Evaluate the questions based on perplexity and print the results
    results = evaluate_questions(data)
    accuracy = sum(results) / len(results)
    with open(output_perplexity_file, "w") as outfile:
        outfile.write(str(accuracy))


