import os
import json

def generate_section_text(selected_capitvlvms):
    folder_path = "../data/llpsi"
    result = []

    for filename in os.listdir(folder_path):
        if "section" in filename:
            capitvlvm_number = filename.split(".")[0].split("_")[1]
            
            if capitvlvm_number in selected_capitvlvms and "en" not in filename:
                with open(os.path.join(folder_path, filename), "r") as file:
                    section_content = file.read().replace("\\", "")
                
                text = {"prompt": f"", "completion": section_content.replace("\n", " ")}
                result.append(json.dumps(text))
    capivlvm_nums = '_'.join(str(item) for item in selected_capitvlvms)
    with open("train_capitvlvm_" + capivlvm_nums + ".jsonl", "w") as file:
        for text in result:
            file.write(text + "\n")

selected_sections = ["1"]  # Specify the section numbers here
generate_section_text(selected_sections)
