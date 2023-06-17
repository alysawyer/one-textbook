import re
import json
import random

def dict_to_jsonl(dictionary, file_path):
    '''converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            json_data = {'prompt': "ANSWER KEY:" + str(value[1]) + " Q: " + key + " A: ", 'completion': str(value[0])}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')

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


output_dict = {}
filename = "ch5.txt"
with open(filename, "r") as file:
    file_text = file.read()

with open(filename, "r") as file:
    for line in file:
        if not line.startswith("#"):
            output_dict.update(whole_word_replacement(line.rstrip("\n"), file_text))
            output_dict.update(suffix_replacement(line.rstrip("\n")))

dict_to_jsonl(output_dict, "ch5_lesstoken_quizzes.jsonl")