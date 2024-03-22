#!/bin/bash

path="packages/pwn.py"

cat main.py > $path
echo -e '\n' >> $path
cat sploit.py >> $path
