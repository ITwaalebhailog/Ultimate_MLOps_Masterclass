#!/bin/bash

echo "Select an Option:"
echo "1) Check disk space"
echo "2) show current user"
echo "3) Show memory Usage"
read -p "Enter your choice (1-3): " CHOICE

case "$CHOICE" in
	1)
		df -h /
		;;
	2)
		whoami
		;;
	3)
		free -m
		;;
	*)
		echo "invalid number"
		;;
esac
