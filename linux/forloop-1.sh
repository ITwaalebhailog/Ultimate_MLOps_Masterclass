#!/bin/bash

for ITEM in "file.txt" "photos" "command.sh"
do
	if [ -f "$ITEM" ]; then
		echo "$ITEM is a regular file"
	else
		echo "$ITEM is not a file"
	fi
done
