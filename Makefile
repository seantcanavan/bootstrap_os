SHELL := /bin/bash


.PHONE: ubuntu python deps

deps:
	source venv/bin/activate && pip install -r requirements.txt

python:
	python3 -m venv venv

ubuntu:
	sudo python3 ubuntu/ubuntu.py
