#!/bin/bash

for NUM in 1 2 3 4 5
do
	if [ $((NUM % 2)) -eq 0 ]; then
		echo "$NUM is Even"
	else
		echo "$NUM is Odd"
	fi
done
