#!/bin/bash

count_to_five() {
	COUNT=1

	while [ $COUNT -le 5 ]; do
		if [ $COUNT -eq 3 ]; then
			echo "Number is $COUNT -- Middle Number"
		elif [ $COUNT -eq 4 ]; then
			echo "Number is $COUNT"
			break
		else
			echo "Number is $COUNT"
		fi
		COUNT=$((COUNT+1))
	done
}

count_to_five
