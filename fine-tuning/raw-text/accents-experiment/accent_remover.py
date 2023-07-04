from unidecode import unidecode

# Read the text file
with open('ch1_5-accents.txt', 'r') as file:
    text = file.read()

# Remove Latin accents
text_without_accents = unidecode(text)

# Write the text without accents to a new file
with open('ch1_5-no_accents.txt', 'w') as file:
    file.write(text_without_accents)
