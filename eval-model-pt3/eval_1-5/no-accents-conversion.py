import os
import json
import unidecode
import shutil

def remove_accents_from_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    for item in json_data:
        # Remove accents from "question" key
        item["question"] = unidecode.unidecode(item["question"])

        # Remove accents from each item in "evalsentences" list
        item["evalsentences"] = [unidecode.unidecode(sentence) for sentence in item["evalsentences"]]

        # Remove accents from "answer" key
        item["answer"] = unidecode.unidecode(item["answer"])

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def create_no_accents_folder(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through the files in the source folder
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        if os.path.isfile(source_path):
            # Remove accents from the JSON file
            output_filename = filename.replace(".no-accents.json", ".json")
            output_path = os.path.join(destination_folder, output_filename)
            remove_accents_from_json_file(source_path, output_path)

# Source folders
source_folder_a = "PENSVMA.accents"
source_folder_b = "PENSVMB.accents"

# Destination folders
destination_folder_a = "PENSVMA.no-accents"
destination_folder_b = "PENSVMB.no-accents"

# Process files in source folder A
create_no_accents_folder(source_folder_a, destination_folder_a)

# Process files in source folder B
create_no_accents_folder(source_folder_b, destination_folder_b)
