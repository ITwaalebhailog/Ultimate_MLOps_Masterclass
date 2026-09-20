#!/bin/bash

check_even_odd() {
	NUMBERS="2 5 8 11"

	for NUM in $NUMBERS; do
		if [ $((NUM % 2)) -eq 0 ]; then
			echo "$NUM is Even"
		else
			echo "$NUM is Odd"
		fi
	done
}

#Calling the function
check_even_odd

