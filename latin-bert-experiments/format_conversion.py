import json

def process_json(json_file_path, output_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    with open(output_file_path, 'w') as output_file:
        for item in data:
            question = item['question']
            eval_sentences = item['evalsentences']
            answer = item['answer']

            # Find the word with the tilde
            word_with_tilde = question.split(' ')[2].replace('~', '')

            # Find the index of the word in the answer, handling punctuation
            word_index = next((i for i, word in enumerate(answer.split()) if word.rstrip('.,') == word_with_tilde), None)

            if word_index is not None:
                # Generate the formatted output
                formatted_output = f"{question.replace(f'{word_with_tilde}~', f'< {word_with_tilde} >')} {eval_sentences[word_index].replace(word_with_tilde, f'< {word_with_tilde} >')}\n"
                
                # Write to the output file
                output_file.write(formatted_output)
            else:
                print(f"Word '{word_with_tilde}' not found in the answer.")


            # Write to the output file
            output_file.write(formatted_output)

if __name__ == "__main__":
    json_file_path = "CAPITVLVM_I.json"  # Replace with the actual path to your JSON file
    output_file_path = "output.txt"  # Replace with the desired output file path

    process_json(json_file_path, output_file_path)
