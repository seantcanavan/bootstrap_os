import os
import subprocess
import sys

output = []


def done(code: int):
    output.append(f"exiting with code {code}\n")
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
        ls_snaps_location = ['sudo', 'systemctl', 'disable', service]
        result = subprocess.run(ls_snaps_location)
        if result != 0:
            output.append(f"Error running command {ls_snaps_location}")
            done(1)
        else:
            output.append(" ".join(ls_snaps_location))

snap_locations = [
    '/var/lib/snapd/snaps',
    '/snap/bin',
]

for location in snap_locations:
    if not os.path.exists(location):
        output.append(f"snap location {location} does not exist. continuing.")
        continue
    ls_snaps_location = ['ls', '-l', location]
    output.append(" ".join(ls_snaps_location))
    installed_snaps = subprocess.run(ls_snaps_location, capture_output=True, text=True).stdout.strip()
    for current_snap in installed_snaps:
        remove_snap_command = ['sudo', 'snap', 'remove', current_snap]
        remove_snap = subprocess.run(remove_snap_command)
        if remove_snap != 0:
            output.append(f"Error running command {remove_snap_command}")
            done(1)
        else:
            output.append(" ".join(remove_snap_command))

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
    ls_snaps_location = [
        'dpkg',
        '-s',
        package
    ]
    str_command = " ".join(ls_snaps_location)
    result = subprocess.run(ls_snaps_location, capture_output=True, text=True)
    if result.returncode != 0:
        install_command = [
            'sudo',
            'apt',
            'install',
            '-y',
            package
        ]
        inner_str_command = " ".join(install_command)
        inner_result = subprocess.run(install_command)
        if inner_result.returncode != 0:
            output.append(f"Error running command {inner_str_command}")
            done(1)
        else:
            output.append(inner_str_command)
    else:
        output.append(str_command)

chrome_deps_to_install = [
    ["wget", "-q", "-O", "-", "https://dl-ssl.google.com/linux/linux_signing_key.pub", "|", "sudo", "apt-key", "add", "-"],
    ["sudo", "sh", "-c", "echo", "http://dl.google.com/linux/chrome/deb/", "stable", "main", ">>", "/etc/apt/sources.list.d/google.list"],
    ["sudo", "apt", "update"],
    ["sudo", "apt-get", "install", "-y", "google-chrome-stable"]
]

for command in chrome_deps_to_install:
    str_command = " ".join(command)
    result = subprocess.run(command)
    if result.returncode != 0 and result.returncode != 4:
        output.append(f"Error running command {str_command}")
        done(1)
    else:
        output.append(str_command)

done(0)
