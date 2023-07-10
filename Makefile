SHELL := /bin/bash

install-system:
	source .env && sudo python3 bootstrap_system_deps.py

install-user:
	source .env && python3 bootstrap_user_deps.py
