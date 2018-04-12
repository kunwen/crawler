#!/bin/sh
pip freeze > requirement.txt
python -m py_compile *.py
python -m py_compile crawler/*.py
mkdir -p work/conf/
mkdir -p work/crawler/
cp -rf main.sh work/
cp -rf one.sh work/
cp -rf requirement.txt work/
cp -rf *.pyc work/
rm -rf *.pyc 
cp -rf README.txt work/
cp -rf test_env work/
cp -rf crawler/*.pyc work/crawler/
cp -rf crawler/*.conf work/crawler/
rm -rf crawler/*.pyc 
cp -rf conf/* work/conf/
zip -r work.zip  work  
rm -rf work

