for dir in quizType*; do
    if [ -d "$dir" ]; then
	python3 lmqltoAccuracy.py "$dir"
    fi
done
