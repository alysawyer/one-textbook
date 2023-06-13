import re
import json

def dict_to_jsonl(dictionary, file_path):
    ''' converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            json_data = {'prompt': key, 'completion': value}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')

def whole_word_replacement(input_string):
    '''takes in one line of the file, outputs a dictionary with the following format for every word in the line:
    key: the line with one word replaced with a tidle
    value: the replaced word'''
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    word_dictionary = {}

    for word in words:
        replaced_sentence = re.sub(r'\b' + word + r'\b', '~', input_string, count=1)  # Replace only the first occurrence of the current word with a tilde (~)
        word_dictionary[replaced_sentence] = word

    return word_dictionary

def suffix_replacement(input_string):
    '''takes in one line of the file, 
    outputs a dictionary with the following format for every word in the line with a common latin suffix:
    key: the line with the word ending replaced with a tidle
    value: the common suffix'''
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    word_dictionary = {}

    latin_suffixes = [
        "us",
        "a",
        "um",
        "i",
        "ae",
        "is",
        "orum",
        "arum",
        "e",
        "es",
        "us",
        "os",
        "is",
        "ei",
        "ei",
        "ium",
        "ibus",
        "er",
        "trix",
        "or",
        "ores",
        "ibus",
        "es",
        "ei",
        "is",
        "ia"
    ]

    for word in words:
        for suffix in latin_suffixes:
            if word.endswith(suffix):
                replaced_sentence = re.sub(r'\b' + word + r'\b', word[:-len(suffix)] + '~', input_string, count=1)  # Replace the suffix with a tilde (~) only once
                word_dictionary[replaced_sentence] = suffix
                break

    return word_dictionary

# helper for every_char_replacement
def check_punctuation_in_string(input_string):
    '''returns true if a string contains no punctuation'''
    for char in input_string:
        if char in string.punctuation:
            return False
    return True

# helper for every_char_replacement
def check_no_alphabet_chars(input_string):
    '''returns true if a string only has characters in the alphabet'''
    return any(char.isalpha() for char in input_string)

def every_char_replacement(input_string, num_chars_removed):
    '''
    takes in string and number of characters max to remove
    returns a dictionary, where  
    values: each line of the string minus every combination of part of each word 
    keys: the missing part of the word where the length is from 1 to the max characters to remove
    '''
    result_dict = {}
    j = num_chars_removed

    for i in range(len(input_string)):
        while j > 0:
            modified_line = line[:i] + '~' * j + line[i+j:]
            value = line[i:j+i]
            if (check_punctuation_in_string(value) and 
                check_no_alphabet_chars(value) and
                " " not in value and 
                len(value) == j):
                result_dict[modified_line.strip('\n')] = value
            j -= 1
        j = num_chars_removed
    
    return result_dict


file_path = "input.txt" #TODO: make more generic 
output_dict = {}
with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith("#"):
                output_dict.update(whole_word_replacement(line.rstrip("\n")))
                output_dict.update(suffix_replacement(line.rstrip("\n")))

dict_to_jsonl(output_dict, "output.jsonl") #TODO: give better output name