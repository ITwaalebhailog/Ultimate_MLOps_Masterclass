#!/bin/bash

read -p "enter day (mon-sun): " DAY


case "$DAY" in
	Sat|Sun)
		echo "Its a weekend"
		;;
	Mon|Tue|Wed|Thu|Fri)
		echo "its a weekday"
		;;
	*)
		echo "Invalid day enetered"
		;;
esac
