for file in "results-capV"/*; do
    # Rename the file
    mv "$filename" "${filename%.json}.0shot.json"
done