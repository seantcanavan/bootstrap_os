import os
import subprocess
import sys
from pprint import pprint

snap_services_to_disable = [
    "snapd.service",
    "snapd.socket",
    "snapd.seeded.service",
]

all_running_services = subprocess.run(['service', '--status-all'], capture_output=True, text=True).stdout.strip()
# print(f"all_services_result: {all_running_services}")

for service in snap_services_to_disable:
    if service in all_running_services:
        # print(f"disabling service: {service}")
        result = subprocess.run(['sudo', 'systemctl', 'disable', service])
        if result != 0:
            print(f"error disabling service: {service}")
            sys.exit(1)

print("Successfully disabled all services in snap_services_to_disable:")
pprint(snap_services_to_disable)

snap_locations = [
    '/var/lib/snapd/snaps',
    '/snap/bin',
]

for location in snap_locations:
    if not os.path.exists(location):
        print(f"location {location} does not exist. continuing.")
        continue
    installed_snaps = subprocess.run(['ls', '-l', location], capture_output=True, text=True).stdout.strip()
    # print(f"installed_snaps: {installed_snaps}")
    for current_snap in installed_snaps:
        remove_snap = subprocess.run(['sudo', 'snap', 'remove', current_snap])
        if remove_snap != 0:
            print("Error uninstalling snap spackage " + current_snap)
            sys.exit(1)

print("Successfully removed all snaps in snap_locations:")
pprint(snap_locations)

apt_packages_to_install = [
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

for package in apt_packages_to_install:
    result = subprocess.run(['dpkg', '-s', package], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(['sudo', 'apt', 'install', '-y', package])

print("Successfully installed all packages in apt_packages_to_install:")
pprint(apt_packages_to_install)
