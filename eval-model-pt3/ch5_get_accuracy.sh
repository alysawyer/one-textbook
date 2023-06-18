for dir in "test-finetune-1"/*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
