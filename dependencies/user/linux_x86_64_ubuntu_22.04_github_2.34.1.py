import json
import os
import subprocess
import sys
from pprint import pprint

from bootstrap_utils import load_env_file

LINUX_SSH_KEY_PATH = "~/.ssh/id_rsa.pub"

if not os.path.exists(".env") and os.path.exists("../../../.env"):
    print("Error: You must set a .env file. Please refer to the example file as a starting template.")
    sys.exit(1)

if os.path.exists(".env"):
    load_env_file(".env")

if os.path.exists("../../../.env"):
    load_env_file(".env")

github_user_name = os.getenv('BOOTSTRAP_GITHUB_USER_NAME')
if github_user_name is None:
    print("Error: the environment variable 'BOOTSTRAP_GITHUB_USER_NAME' must be set.")

github_user_email = os.getenv('BOOTSTRAP_GITHUB_USER_EMAIL')
if github_user_email is None:
    print("Error: the environment variable 'BOOTSTRAP_GITHUB_USER_EMAIL' must be set.")

github_personal_api_pat = os.getenv('BOOTSTRAP_GITHUB_PERSONAL_API_PAT')
if github_personal_api_pat is None:
    print("Error: the environment variable 'BOOTSTRAP_GITHUB_PERSONAL_API_PAT' must be set.")

github_org_repo_pat = os.getenv('BOOTSTRAP_GITHUB_ORG_REPO_PAT')
if github_org_repo_pat is None:
    print("WARN: No PAT set for accessing your internal repos. Will not override git URL in .gitconfig.")

if not os.path.exists(LINUX_SSH_KEY_PATH):
    print("Generating public/private key pair since none exists")
    command = ["ssh-key", "-t", "rsa", "-b", "4096", "-C", github_user_email, "-f", "~/.ssh/id_rsa", "-N", "\"\""]
    output = subprocess.run(command, capture_output=True, text=True)
    if output.returncode != 0:
        print(f"Got non zero return code {output.returncode}")
    if not os.path.exists(LINUX_SSH_KEY_PATH):
        print("Creating ssh-key failed. Exiting.")
        sys.exit(1)
    print("successfully created an ssh-key for you. please add it to github before continuing.")
    with open(LINUX_SSH_KEY_PATH, "r") as file:
        contents = file.read()
    print(contents)
    choice = input("Please type any key when you have finished adding this SSH key to your github account")

if github_org_repo_pat is not None:
    print("Configuring your org-wide PAT")
    command = ["git", "config", "--global", 'url."https://' + github_user_name + ":" + github_org_repo_pat + '@github.com".insteadOf "https://github.com"']
    output = subprocess.run(command, capture_output=True, text=True)
    print("successfully added PAT to .gitconfig")
    pprint(output)

make_home_dir = ["mkdir", "-p", "~/code/github.com"]
make_directory_output = subprocess.run(make_home_dir)

get_github_user_repos_command = ["curl", "-i", "-u", "seantcanavan", "https://api.github.com/users/" + github_user_name + "/repos"]

repo_command_output = subprocess.run(get_github_user_repos_command, capture_output=True, text=True, shell=True)
pprint(json.loads(repo_command_output.stdout))
