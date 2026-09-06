#!/bin/bash

#$0 == Name os the script
#$1, $2, $3 == First.second and third arguments passed
#$# == total counts of arguments we have passed
#$$ == process id of the current scipt
#$? == exit status of the current

echo "Script: $0"
echo "Target Service: $1 $7"
echo "Target Action: $2"
echo "Total Inputs: $#"
echo "Process ID: $$"
echo "Exit status: $?"

systemctl status $1
