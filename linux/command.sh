#!/bin/bash

# User defined varibles

SERVER_NAME="Production-01"
echo "Deploying to $SERVER_NAME"

#SYSTEM Variables

echo "Current user: $USER"
echo "User home directory: $HOME"

# Variable Subsitution

ROLE="Admin"
echo "Welcome ${ROLE}"

#Command Subisitution

TODAY=$(date)
DISK_FREE=$(df -h)

echo "Todays' date is $TODAY"
echo "Some SPace is remaining on my machine $DISK_FREE"
