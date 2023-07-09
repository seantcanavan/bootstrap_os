import os
import subprocess
import sys

from bootstrap_utils import load_env_file

if not os.path.exists(".env"):
    print("Error: You must set a .env file. Please refer to the example file as a starting template.")
    sys.exit(1)

load_env_file(".env")

# Get the user's name and email from environment variables
user_name = os.getenv('BOOTSTRAP_GIT_USER_NAME')
user_email = os.getenv('BOOTSTRAP_GIT_USER_EMAIL')

# If either variable is not set, print an error and exit
if user_name is None or user_email is None:
    print("Error: The environment variables 'user_name' and 'user_email' must be set.")
    sys.exit(1)

# Define the commands to run
commands = [
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
