import os
import subprocess
import sys

from bootstrap_utils import load_env_file

if not os.path.exists(".env") and os.path.exists("../../../.env"):
    print("Error: You must set a .env file. Please refer to the example file as a starting template.")
    sys.exit(1)

if os.path.exists(".env"):
    load_env_file(".env")

if os.path.exists("../../../.env"):
    load_env_file(".env")

# Get the user's name and email from environment variables
git_user_name = os.getenv('BOOTSTRAP_GIT_USER_NAME')
if git_user_name is None:
    print("Error: the environment variable 'BOOTSTRAP_GIT_USER_NAME' must be set.")

git_user_email = os.getenv('BOOTSTRAP_GIT_USER_EMAIL')
if git_user_email is None:
    print("Error: the environment variable 'BOOTSTRAP_GIT_USER_EMAIL' must be set.")

# Define the commands to run
commands = [
    ['git', 'config', '--global', 'user.name', git_user_name],
    ['git', 'config', '--global', 'user.email', git_user_email],
    ['git', 'config', '--global', '--add', '--bool', 'push.autoSetupRemote' 'true'],
]

# Execute each command
for command in commands:
    process = subprocess.Popen(command)
    output, error = process.communicate()

    if error is not None:
        print(f"An error occurred: {error}")
    else:
        print(f"Command '{' '.join(command)}' executed successfully")
