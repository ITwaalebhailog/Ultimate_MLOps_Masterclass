#!/bin/bash

# user defined input

read -p " Enter student name: " Student_name
read -p " Enter score (0-100): " Score

if [ -z "$Student_name" ] || [ -z "$Score" ]; then
	echo "[ERROR] Both name and Score are required"
	exit 1
fi

if [ "$Score" -ge 90 ]; then
	Grade="A" 
elif [ "$Score" -ge 75 ]; then
	Grade="B"
elif [ "$Score" -ge 50 ]; then
	Grade="C"
else
	Grade="Fail"
fi

echo "Result: $Student_name recieved grade: $Grade"

if [ "$Grade" == "Fail" ]; then
	echo "Notice: Students needs to focus more"
else
	echo "Notice: "$Student_name" passed succesfully"
fi
