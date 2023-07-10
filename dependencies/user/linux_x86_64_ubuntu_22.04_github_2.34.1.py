import os
import subprocess
import sys

from bootstrap_utils import load_env_file

output = []


def done(code: int):
    output.append(f"exiting with code 12{code}\n")
    with open(os.path.basename(__file__) + ".txt", "w") as file:
        file.write("\n".join(output))
    sys.exit(code)


load_env_file("../../.env")

LINUX_SSH_KEY_PATH = os.path.expanduser('~') + "/.ssh/id_rsa.pub"

github_user_name = os.getenv('BOOTSTRAP_GITHUB_USER_NAME')
if github_user_name is None:
    output.append("Error: the environment variable 'BOOTSTRAP_GITHUB_USER_NAME' must be set.")
    done(1)

github_user_email = os.getenv('BOOTSTRAP_GITHUB_USER_EMAIL')
if github_user_email is None:
    output.append("Error: the environment variable 'BOOTSTRAP_GITHUB_USER_EMAIL' must be set.")
    done(1)

github_personal_api_pat = os.getenv('BOOTSTRAP_GITHUB_PERSONAL_API_PAT')
if github_personal_api_pat is None:
    output.append("Error: the environment variable 'BOOTSTRAP_GITHUB_PERSONAL_API_PAT' must be set.")
    done(1)

github_org_repo_pat = os.getenv('BOOTSTRAP_GITHUB_ORG_REPO_PAT')
if github_org_repo_pat is None:
    output.append("WARN: No PAT set for accessing your internal repos. Will not override git URL in .gitconfig.")

commands = [
    ["mkdir", "-p", os.path.expanduser('~') + "/code/github.com"],
]

if not os.path.exists(LINUX_SSH_KEY_PATH):
    output.append("Generating public/private key pair since none exists")
    commands.append(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", github_user_email, "-f", os.path.expanduser("~") + "/.ssh/id_rsa", "-N", "\"\""])

if github_org_repo_pat is not None:
    output.append("Github Org Repo PAT is set. Will configure .gitconfig to override calls to github.com with your PAT")
    github_pat_command = [
        'git',
        'config',
        '--global',
        f'url.https://{github_user_name}:{github_org_repo_pat}.insteadOf',
        'https://github.com'
    ]
    commands.append(github_pat_command)

for command in commands:
    str_command = " ".join(command)
    result = subprocess.run(command)
    if result.returncode != 0:
        output.append(f"Error running command {str_command}")
        done(1)
    else:
        output.append(str_command)

github_commands = [
    ["curl", "-u", f"{github_user_name}:{github_personal_api_pat}", f"https://api.github.com/user/repos"],
]

for command in github_commands:
    output.append(command)
    str_command = " ".join(command)
    result = subprocess.run(command)
    if result.returncode != 0:
        output.append(f"Error running command {str_command}")
        done(1)
    output.append(str_command)
    output.append("hi sean")
    api_output = result.stdout.strip()
    output.append(api_output)

done(0)
