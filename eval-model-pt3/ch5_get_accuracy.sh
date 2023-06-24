for dir in "imtired1"/*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
