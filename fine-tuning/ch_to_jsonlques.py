import re
import json
import os

def dict_to_jsonl(dictionary, file_path):
    ''' converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            json_data = {'prompt': "Answer key: " + str(value[1]) + " Q: " + key + " A: ", 'completion': str(value[0])}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')

def whole_word_replacement(input_string):
    '''takes in one line of the file, outputs a dictionary with the following format for every word in the line:
    key: the line with one word replaced with a tidle
    value: the replaced word'''
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    word_dictionary = {}

    for word in words:
        word_bank = ["list of random 10 words in the chapter here"]
        replaced_sentence = re.sub(r'\b' + word + r'\b', '~', input_string, count=1)  # Replace only the first occurrence of the current word with a tilde (~)
        word_dictionary[replaced_sentence] = [word, word_bank]

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
                word_dictionary[replaced_sentence] = [suffix, latin_suffixes]
                break

    return word_dictionary


folder_path = "../data/llpsi"
selected_capitvlvms = [1]
output_dict = {}

# for filename in os.listdir(folder_path):
#     if "section" in filename:
#         capitvlvm_number = filename.split(".")[0].split("_")[1]
#         if int(capitvlvm_number) in selected_capitvlvms and "en" not in filename:
#             with open(os.path.join(folder_path, filename), "r") as file:
#                 for line in file:
#                     if not line.startswith("#"):
#                         output_dict.update(whole_word_replacement(line.rstrip("\n")))
#                         output_dict.update(suffix_replacement(line.rstrip("\n")))

#                 dict_to_jsonl(output_dict, "ch" + capitvlvm_number + "_ quizzes.jsonl") 
filename = "ch5.txt"
with open(filename, "r") as file:
    for line in file:
        if not line.startswith("#"):
            output_dict.update(whole_word_replacement(line.rstrip("\n")))
            output_dict.update(suffix_replacement(line.rstrip("\n")))

dict_to_jsonl(output_dict, filename + "_QA_quizzes.jsonl")
