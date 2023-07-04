import re

# Function to split text into sentences
def split_sentences(text):
    # Use regular expressions to split text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s(?!\n)', text)
    return sentences

# Read the text file
with open('ch1to5-no-accent-lines.txt', 'r') as file:
    text = file.read()

# Split text into sentences
sentences = split_sentences(text)

# Write the sentences to a new file
with open('ch1to5-no-accent-lines.txt', 'w') as file:
    for sentence in sentences:
        file.write(sentence + '\n')
