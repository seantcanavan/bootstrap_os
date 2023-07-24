import os
import subprocess

debug = True


def prt_plus(to_print: str):
    print(to_print + "\n")


def exec_print(command: [str], quiet: bool = None) -> int:
    output = subprocess.run(command)
    code = output.returncode
    if not quiet:
        prt_plus(f"code: {code} com: {' '.join(command)}")
    return code


def exec_strip_split(command: [str], quiet: bool = None, split_char: str = None, split_index: int = None):
    if debug:
        prt_plus(' '.join(command))
    output = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    if split_char is not None:
        output = output.split(split_char)
    if split_index is not None:
        return output[split_index]
    return output


os.environ["HOME"] = "/home/userwork"
logged_in_user = "userwork"

# github_classic = input("Enter your github classic token. This will be used to download all of your repos. ")
# github_signing_key = input("Enter your github signing key. This will be used to enable signed git commits.")

user_name = "Sean T Canavan"
user_email = "seantcanavan@gmail.com"
