for dir in "CAPITVLVM_V"/*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
