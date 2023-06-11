import os
import asyncio
import lmql
import json
from pathlib import Path
import argparse
import aiometer
from functools import partial

async def query(c):
    '''takes in a dict that includes lmql prompt and the true answer,
    returns 1 if the model is correctand 0 if wrong'''
    print("sending output")
    output = (await lmql.run(c["code"], output_writer=lmql.stream("RESPONSE")))
    if output[0].variables['ANSWER'].strip() == c["answer"]:
        print("output returned, answer is : 1")
        return 1
    print("output returned, answer is : 0")
    return 0

async def run(codes):
    results = await aiometer.run_all([partial(query,c) for c in codes], max_per_second=.2, max_at_once=5)
    return results

def calc_accuracy(codes):
    '''calculates accuracy based on outputs from query
    >>> calc_accuracy([{'code': ('argmax "Q: Fill in the missing words: Italia ~ Europa est; Graecia ~ in Europa est. '
    ...                 'Answer Choices: (A) in quoque (B) ne non (C) ubi (D) non sed '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B","C", "D"]'),'answer': 'A'}, {'code': ('argmax' 
    ...                 '"Q: Fill in the missing words: ~ est Arabia? In Asia est Arabia. '
    ...                 'Answer Choices: (A) in quoque (B) ne non (C) ubi (D) non sed '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B","C", "D"]'),'answer':'C'}])
    0.5
    >>> calc_accuracy([{'code': ('argmax "Q: Fill in the tilde: Italia in Europa ~. '
    ...                 'Answer Choices: (A) est (B) sunt '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B"]'),'answer': 'A'}, {'code': ('argmax'
    ...                 '"Q: Fill in the tilde: Italia et Gallia in Europa ~. '
    ...                 'Answer Choices: (A) est (B) sunt '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B"]'),'answer':'B'}])
    1.0
    '''
    # using query to prompt model with questions in parallel 
    loop = asyncio.get_event_loop()
    
    results = loop.run_until_complete(run(codes))
    return round(sum(results)/len(results), 2)

def main():
    # opening json file
    parser = argparse.ArgumentParser()
    parser.add_argument('second_argument')

    file_path = Path.cwd()/parser.parse_args().second_argument
    with file_path.open(mode='r',encoding="utf-8") as f:
         data = json.load(f)

    # parser.add_argument('third_argument')
    # print(Path.cwd()/parser.parse_args().second_argument,parser.parse_args().third_argument)
    
    file_path = Path.cwd()/parser.parse_args().second_argument
    with file_path.open(mode='r',encoding="utf-8") as f:
        data = json.load(f)
    info_list = parser.parse_args().second_argument.split(".")
    print(info_list)
    
    json_name = ".".join([info_list[0].split("/")[2], info_list[3], info_list[1], info_list[2], info_list[0].split("/")[1], info_list[4]])
    
    print(json_name)
    with open("results/" + json_name, "w") as outfile:
         outfile.write(str(calc_accuracy(data["codes"])))

if __name__ == "__main__":
    main()
