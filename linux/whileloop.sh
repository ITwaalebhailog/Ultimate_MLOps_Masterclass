#!/bin/bash

Count=3

while [ $Count -gt 0 ]
do
	if [ $Count -gt 1 ]; then
	        echo "$Count.... almost ready"
        else
		echo "$Count..."
	fi
	Count=$((Count - 1))
done
echo "Blastoff!"

#for i in 1..5
#do
	#echo "$i"
