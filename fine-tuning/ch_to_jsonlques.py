import re
import json
import random
import numpy as np


def dict_to_jsonl_0shot(dictionary, file_path):
    '''converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            json_data = {'prompt': "ANSWER KEY:" + str(value[1]) + " Q: " + key + " A: ", 'completion': str(value[0])}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')

def dict_to_jsonl_1shot(dictionary, example_line, file_path, file_text):
    '''converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            formatted_example_line = create_shot_examples(example_line, value[2], file_text)
            json_data = {'prompt': formatted_example_line + " ANSWER KEY:" + str(value[1]) + " Q: " + key + " A: ", 'completion': str(value[0])}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')

def create_shot_examples(example_line, whole_or_partial, file_text):
    output_dict = {}
    if whole_or_partial == "w":
        output_dict = whole_word_replacement(example_line, file_text)
    else:
        output_dict = suffix_replacement(example_line)    


    
    dict_key = str(list(output_dict.keys())[0])

    print(output_dict[dict_key])
    print("ANSWER KEY:" + str(output_dict[dict_key][1]) + " Q: " + dict_key + " A: " +  str(output_dict[dict_key][0]))
    return "ANSWER KEY:" + str(output_dict[dict_key][1]) + " Q: " + dict_key + " A: " +  str(output_dict[dict_key][0])

    return "meow"
    return "ANSWER KEY:" + output_dict.values()[1] + " Q: " + output_dict.keys()[0] + " A: " + output_dict.values()[0]

def create_word_bank(file_text, num):
    '''creates a list of num random words from file_text'''
    words = re.findall(r'\b\w+\b', file_text)
    random_words = random.sample(words, num)
    return random_words


def whole_word_replacement(input_string, file_text):
    '''takes in one line of the file, outputs a dictionary with the following format for every word in the line:
    key: the line with one word replaced with a tidle
    value: the replaced word'''
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    word_dictionary = {}

    for word in words:
        word_bank = create_word_bank(file_text, 9)
        word_bank.append(word)
        random.shuffle(word_bank)
        
        replaced_sentence = re.sub(r'\b' + word + r'\b', '~', input_string, count=1)  # Replace only the first occurrence of the current word with a tilde (~)
        word_dictionary[replaced_sentence] = [word, word_bank, "w"]

    return word_dictionary

def suffix_replacement(input_string):
    '''takes in one line of the file, 
    outputs a dictionary with the following format for every word in the line with a common latin suffix:
    key: the line with the word ending replaced with a tidle
    value: the common suffix'''
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    word_dictionary = {}

    # suffixes in ch5
    latin_suffixes = ['am', 'ds', 'iunt', 'e', 'ete', 'o', 'os', 'unt', 'et', 'ate', 'a', 'ant', 'at', 'i', 'is', 'it', 'ent', 'ite', 'as']

    for word in words:
        for suffix in latin_suffixes:
            if word.endswith(suffix):
                replaced_sentence = re.sub(r'\b' + word + r'\b', word[:-len(suffix)] + '~', input_string, count=1)  # Replace the suffix with a tilde (~) only once
                word_dictionary[replaced_sentence] = [suffix, latin_suffixes, "r"]
                break

    return word_dictionary


output_dict = {}
filename = "ch5.txt"
with open(filename, "r") as file:
    file_text = file.read()

with open(filename, "r") as file:
    # split the file randomly in half
    # for line in 1 half, for line in second half, 
    lines = file.readlines()
    example_lines, eval_lines = np.array_split(lines, 2)
    random.shuffle(lines)
    for eval_line in eval_lines:
        if not eval_line.startswith("#") or example_line.startswith("#"):
            output_dict.update(whole_word_replacement(eval_line.rstrip("\n"), file_text))
            output_dict.update(suffix_replacement(eval_line.rstrip("\n")))

for example_line in example_lines:
    dict_to_jsonl_1shot(output_dict, example_line, "ch5_lesstoken_quizzes_1shot.jsonl", file_text)