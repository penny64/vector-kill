@ECHO OFF

python freeze.py py2exe
copy *.png dist
copy *.ttf dist
