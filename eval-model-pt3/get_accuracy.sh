for dir in "davinci"/*; do
	for FILE in "$dir"/*; do 
		python3 get_accuracy.py $FILE
		done
done
