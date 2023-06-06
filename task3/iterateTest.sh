for dir in PENSVM-*; do
    if [ -d "$dir" ]; then
	python3 iterateTest.py "$dir"
    fi
done
