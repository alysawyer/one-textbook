for dir in "1_0_shot_finetune_test"/*; do
	for FILE in "$dir"/*; do 
		python get_accuracy.py $FILE
		done
done
