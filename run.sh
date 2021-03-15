#!/bin/bash

SCRIPT_HOME="/home/jake/Code/fortireleases"

cd $SCRIPT_HOME

date >> log.txt

source ./venv/bin/activate

python3 main.py
