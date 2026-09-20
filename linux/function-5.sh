#!/bin/bash

double_number() {
	NUM=15
	RESULT=$((NUM * 2))

	echo "$RESULT"
}

ANSWER=$(double_number)
echo " The returned value is: $ANSWER "

if [ "$ANSWER" -gt 20 ]; then
	echo " the calculated result is large "
else
	echo " the calculated is result is small"
fi
