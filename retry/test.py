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

apt_setup_commands = []

if "VGA compatible controller: NVIDIA Corporation" in exec_strip_split(["lspci"]):
    apt_setup_commands.append(["wget",
                               "https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda-repo-ubuntu2204-12-2-local_12.2.0-535.54.03-1_amd64.deb"])
    apt_setup_commands.append(["sudo", "dpkg", "-i", "cuda-repo-ubuntu2204-12-2-local_12.2.0-535.54.03-1_amd64.deb"])
    apt_setup_commands.append(
        ["sudo", "cp", "/var/cuda-repo-ubuntu2204-12-2-local/cuda-*-keyring.gpg", "/usr/share/keyrings/"])

prt_plus("Performing package setup commands")
for setup_command in apt_setup_commands:
    exec_print(setup_command)
