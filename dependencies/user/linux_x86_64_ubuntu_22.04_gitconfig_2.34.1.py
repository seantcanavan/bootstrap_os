import os
import subprocess
import sys

output = []


def done(code: int):
    output.append(f"exiting with code {code}\n")
    with open(os.path.basename(__file__) + ".txt", "w") as file:
        file.write("\n".join(output))
    sys.exit(code)


# Get the user's name and email from environment variables
git_user_name = os.getenv('BOOTSTRAP_GIT_USER_NAME')
if git_user_name is None:
    output.append("Error: the environment variable 'BOOTSTRAP_GIT_USER_NAME' must be set.")
    done(1)

git_user_email = os.getenv('BOOTSTRAP_GIT_USER_EMAIL')
if git_user_email is None:
    output.append("Error: the environment variable 'BOOTSTRAP_GIT_USER_EMAIL' must be set.")
    done(1)

# Define the commands to run
commands = [
    ['git', 'config', '--global', 'user.name', git_user_name],
    ['git', 'config', '--global', 'user.email', git_user_email],
    ['git', 'config', '--global', '--add', '--bool', 'push.autoSetupRemote', 'true'],
]

for command in commands:
    str_command = " ".join(command)
    result = subprocess.run(command)
    if result.returncode != 0:
        output.append(f"Error running command {str_command}")
        done(1)
    else:
        output.append(str_command)

done(0)
