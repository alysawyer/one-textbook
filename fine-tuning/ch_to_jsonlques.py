import string
import json

def check_punctuation_in_string(input_string):
    '''returns true if a string contains no punctuation'''
    for char in input_string:
        if char in string.punctuation:
            return False
    return True

def check_no_alphabet_chars(input_string):
    '''returns true if a string only has characters in the alphabet'''
    return any(char.isalpha() for char in input_string)

def process_text_file(file_path, num_chars_removed):
    '''
    takes in string and number of characters max to remove
    returns a dictionary, where  
    values: each line of the string minus every combination of part of each word 
    keys: the missing part of the word where the length is from 1 to the max characters to remove
    '''
    result_dict = {}
    j = num_chars_removed
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith("#"):
                for i in range(len(line)):
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

def write_dict_to_jsonl(dictionary, file_path):
    ''' converts the dictionary to jsonl format for openai api'''
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            json_data = {'prompt': key, 'completion': value}
            json_line = json.dumps(json_data)
            file.write(json_line + '\n')


file_path = 'input.txt' 
write_dict_to_jsonl(process_text_file(file_path, 10), 'output.jsonl')