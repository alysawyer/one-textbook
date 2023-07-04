for dir in "full_eval_no_accent"/*; do
	for FILE in "$dir"/*; do 
		python3 get_perplexity-ft.py $FILE
		done
done
