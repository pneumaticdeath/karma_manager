#!/bin/bash

url='https://users.cs.duke.edu/~ola/ap/linuxwords'

curl -s "${url}" | tr 'A-Z' 'a-z' | tr -cd 'a-z\n' | sort -u > dict.txt
