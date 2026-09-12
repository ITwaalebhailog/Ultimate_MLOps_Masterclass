#!/bin/bash

TRIES=1

while [ $TRIES -le 3 ]
do
	read -p "Enter password: " PASS
	if [ "$PASS" = "secret" ]; then
		echo "Acces Granted!"
		break
	else
		echo "Incorrect. ATTEMPT $TRIES of 3"
	fi
	TRIES=$((TRIES + 1))
done

echo "tell me the status"

#break == it will throw me out of the loop
#exit == it will throw me out of the program
#contine == it will skip the stage


for i in 1 2 3 4 5
do
	if [ "$i" -eq 3 ]; then
		echo "skipping the stage"
		continue
	else
		echo "$i"
	fi
done

