import os
import subprocess
import sys




for package in apt_packages_to_install:
    print("attemping to install " + str(package))
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
        print("package " + str(package) + " is already installed. moving on.")
        apt_packages_to_install.remove(package)
