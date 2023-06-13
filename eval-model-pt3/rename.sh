
# folder_path="results-capV"

for file in "$folder_path"/*.json; do
    new_filename=$(echo "$file" | sed 's/\.json$/.0shot.json/')
    mv "$file" "$new_filename"
done