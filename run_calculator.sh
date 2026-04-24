#!/bin/bash

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed. Please install Python 3."
    exit 1
fi

python3 "$(dirname "$0")/calculator.py"
