#!/bin/bash

check_fruits() {
	FRUITS="apple mango banana orange"

	for ITEM in $FRUITS; do
		if [ "$ITEM" = "mango" ]; then
			echo "$ITEM is the king of fruits"
		else
			echo "$ITEM is a regular fruit"
		fi
	done
}

check_fruits
