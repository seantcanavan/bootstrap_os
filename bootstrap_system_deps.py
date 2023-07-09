import os
import sys

from executor import Executor

if os.geteuid() == 0:
    print("The script is running with sudo permissions.")
    prompt = input("Do you wish to continue? (y/n): ")
    if not prompt.lower().startswith("y"):
        print("Script execution canceled.")
        sys.exit(0)
else:
    print("This script requires sudo to run.")
    sys.exit(1)

Executor(False, 'dependencies/system/deps.csv')
