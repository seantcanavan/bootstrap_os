import os
import subprocess

packages = [
    "build-essential",
    "cuda",
    "cuda-keyring",
    "curl",
    "discord",
    "firefox",
    "font-manager",
    "git",
    "guake",
    "libfuse2",
    "nvidia-gds",
    "pinta",
    "silversearcher-ag",
    "slack-desktop",
    "sublime-text",
    "ubuntu-restricted-extras"
]


def check_package_installed(current_package):
    result = subprocess.run(['dpkg', '-s', current_package], capture_output=True, text=True)
    return result.returncode == 0


def install_package(current_package):
    subprocess.run(['sudo', 'apt', 'install', '-y', current_package])


for package in packages:
    if check_package_installed(package):
        print(f"{package} is already installed.")
    else:
        print(f"Installing {package}...")
        install_package(package)
        print(f"{package} is installed.")

print("Done with " + str(os.path.basename(os.path.abspath(__file__))))
