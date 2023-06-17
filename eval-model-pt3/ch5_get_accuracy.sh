for dir in "lowtokenlmql"/*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
