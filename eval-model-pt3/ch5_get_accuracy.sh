for dir in "style4-finetune-test"/*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
