import os
import subprocess

# Get the user's name and email from environment variables
user_name = os.getenv('user_name')
user_email = os.getenv('user_email')

# If either variable is not set, print an error and exit
if user_name is None or user_email is None:
    print("Error: The environment variables 'user_name' and 'user_email' must be set.")
    exit(1)

# Define the commands to run
commands = [
    ['sudo', 'apt-get', 'install', 'git'],
    ['git', 'config', '--global', 'user.name', user_name],
    ['git', 'config', '--global', 'user.email', user_email],
]

# Execute each command
for command in commands:
    process = subprocess.Popen(command)
    output, error = process.communicate()

    if error is not None:
        print(f"An error occurred: {error}")
    else:
        print(f"Command '{' '.join(command)}' executed successfully")
