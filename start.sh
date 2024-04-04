#!/bin/sh
python src/parser.py &
python src/update.py &
wait