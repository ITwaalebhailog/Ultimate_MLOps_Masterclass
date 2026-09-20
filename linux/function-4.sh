#!/bin/bash

check_config_file() {
	FILE="text.sh"
	if [ -f "$FILE" ]; then
		return 0
	else
		return 1
	fi
}

if check_config_file; then
	echo "Success : File exist"
else
	echo "ERROR : File doesn't exist"
fi
