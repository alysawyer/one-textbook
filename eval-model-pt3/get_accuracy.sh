script_dir=$(dirname "$(readlink -f "$0")")

for dir in "$script_dir/davinci"/*; do
    if [ -d "$dir" ]; then
	    for FILE in "$dir"/*; do 
	    	python3 get_accuracy.py $FILE $dir 
    	    done
    fi
done
