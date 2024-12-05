SHELL := /bin/bash


.PHONE: ubuntu python deps

deps:
	source .venv/bin/activate && pip install -r requirements.txt

freeze:
	source .venv/bin/activate && pip freeze -> requirements.txt

pip:
	source .venv/bin/activate && pip install --upgrade pip

python:
	python3 -m venv venv

ubuntu:
	sudo /home/userhome/code/github.com/seantcanavan/bootstrap_os/.venv/bin/python3 ubuntu.py
