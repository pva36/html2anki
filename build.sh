!#/usr/bin/env sh

# activate virtual enviroment
source .venv/bin/activate

pyinstaller main.py -F -n html2anki
