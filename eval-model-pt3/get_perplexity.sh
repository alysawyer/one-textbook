for dir in "perplexing"/*; do
	for FILE in "$dir"/*; do 
		python3 get_perplexity.py $FILE
		done
done
