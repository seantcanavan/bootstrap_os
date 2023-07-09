import os
import subprocess
import sys

from dependency import parse_deps

if os.geteuid() == 0:
    print("This script DOES NOT REQUIRE sudo to run. DO NOT RUN IT WITH SUDO. EVER. THAT WOULD BE BAD.")
    sys.exit(1)

else:
    print("The script is running with sudo permissions.")
    prompt = input("Do you wish to continue? (y/n): ")
    if not prompt.lower().startswith("y"):
        print("Script execution canceled.")
        sys.exit(0)

deps = parse_deps('dependencies/user/deps.csv')

for dep in deps:
    subprocess.run(["python3", dep.file_name])
