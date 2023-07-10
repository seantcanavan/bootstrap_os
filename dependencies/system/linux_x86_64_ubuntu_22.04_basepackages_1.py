import os
import subprocess
import sys

output = []


def done(code: int):
    output.append(f"exiting with code {code}")
    with open(os.path.basename(__file__) + ".txt", "w") as file:
        file.write("\n".join(output))
    sys.exit(code)


snap_services_to_disable = [
    "snapd.service",
    "snapd.socket",
    "snapd.seeded.service",
]

all_running_services = subprocess.run(['service', '--status-all'], capture_output=True, text=True).stdout.strip()

for service in snap_services_to_disable:
    if service in all_running_services:
        command = ['sudo', 'systemctl', 'disable', service]
        output.append(" ".join(command))
        result = subprocess.run(command)
        if result != 0:
            output.append(f"error disabling service: {service}")
            done(1)

snap_locations = [
    '/var/lib/snapd/snaps',
    '/snap/bin',
]

for location in snap_locations:
    if not os.path.exists(location):
        output.append(f"snap location {location} does not exist. continuing.")
        continue
    installed_snaps = subprocess.run(['ls', '-l', location], capture_output=True, text=True).stdout.strip()
    for current_snap in installed_snaps:
        command = ['sudo', 'snap', 'remove', current_snap]
        output.append(" ".join(command))
        remove_snap = subprocess.run(command)
        if remove_snap != 0:
            output.append(f"Error uninstalling snap spackage {current_snap}")
            done(1)

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
    command = [
        'dpkg',
        '-s',
        package
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        install_command = [
            'sudo',
            'apt',
            'install',
            '-y',
            package
        ]
        output.append(" ".join(install_command))
        subprocess.run(install_command)
    else:
        output.append(f"package {package} is already installed.")

done(0)
