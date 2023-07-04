# Read the text file
with open('ch1to5-accent-lines.txt', 'r') as file:
    lines = file.readlines()

# Remove blank lines
lines = [line.strip() for line in lines if line.strip()]

# Write the non-blank lines to a new file
with open('ch1to5-accent-lines.txt', 'w') as file:
    file.write('\n'.join(lines))
