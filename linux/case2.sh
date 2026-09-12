#!/bin/bash

read -p "Enter traffic light color: " COLOR

case "$COLOR" in
	red)
		echo "STOP!"
		;;
	yellow)
		echo "Slow down!"
		;;
	green)
		echo "GO!"
		;;
	*)
		echo "Unknown Signal"
		;;
esac
