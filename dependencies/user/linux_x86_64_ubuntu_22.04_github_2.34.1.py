import json
import os
import subprocess
import sys
from pprint import pprint

from bootstrap_utils import load_env_file

load_env_file("../../.env")

LINUX_SSH_KEY_PATH = os.path.expanduser('~') + "/.ssh/id_rsa.pub"

github_user_name = os.getenv('BOOTSTRAP_GITHUB_USER_NAME')
if github_user_name is None:
    print("Error: the environment variable 'BOOTSTRAP_GITHUB_USER_NAME' must be set.")
    sys.exit(1)

github_user_email = os.getenv('BOOTSTRAP_GITHUB_USER_EMAIL')
if github_user_email is None:
    print("Error: the environment variable 'BOOTSTRAP_GITHUB_USER_EMAIL' must be set.")
    sys.exit(1)

github_personal_api_pat = os.getenv('BOOTSTRAP_GITHUB_PERSONAL_API_PAT')
if github_personal_api_pat is None:
    print("Error: the environment variable 'BOOTSTRAP_GITHUB_PERSONAL_API_PAT' must be set.")
    sys.exit(1)

github_org_repo_pat = os.getenv('BOOTSTRAP_GITHUB_ORG_REPO_PAT')
if github_org_repo_pat is None:
    print("WARN: No PAT set for accessing your internal repos. Will not override git URL in .gitconfig.")

commands = [
    ["mkdir", "-p", os.path.expanduser('~') + "/code/github.com"],
]

if not os.path.exists(LINUX_SSH_KEY_PATH):
    f = os.path.isfile(os.path.expanduser("~") + "/.ssh/id_rsa.pub")
    print("Generating public/private key pair since none exists")
    commands.append(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", github_user_email, "-f", os.path.expanduser("~") + "/.ssh/id_rsa", "-N", "\"\""])

if github_org_repo_pat is not None:
    github_pat_command = [
        'git',
        'config',
        '--global',
        f'url.https://{github_user_name}:{github_org_repo_pat}.insteadOf',
        'https://github.com'
    ]
    commands.append(github_pat_command)

for command in commands:
    print(f"command is {command}")
    process = subprocess.Popen(command)
    output, error = process.communicate()

    if error is not None:
        print(f"An error occurred: {error}")
    else:
        print(f"Command '{' '.join(command)}' executed successfully")

if github_personal_api_pat is not None:
    command = [
        'curl',
        '-H',
        f'Authorization: token {github_personal_api_pat}',
        f'https://api.github.com/user/{github_user_name}/repos'
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    repos = json.loads(output.decode('utf-8'))
    pprint(repos)
    x = 4
