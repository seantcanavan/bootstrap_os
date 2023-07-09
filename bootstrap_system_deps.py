import os
import subprocess
import sys

from dependency import parse_deps

if os.geteuid() == 0:
    print("The script is running with sudo permissions.")
    prompt = input("Do you wish to continue? (y/n): ")
    if not prompt.lower().startswith("y"):
        print("Script execution canceled.")
        sys.exit(0)
else:
    print("This script requires sudo to run.")
    sys.exit(1)

deps = parse_deps('dependencies/system/deps.csv')

for dep in deps:
    subprocess.run(["python3", dep.file_name])
