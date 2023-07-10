import os
import subprocess
import sys

from bootstrap_utils import load_env_file
from dependency import parse_deps


class Executor:
    def __init__(self, debug: bool, deps_file: str):
        self.debug = debug
        self.deps_file = deps_file
        self.base_path = deps_file[0:deps_file.rfind("/") + 1]

        if not os.path.exists(".env"):
            print("Error: You must set a .env file. Please refer to the example file as a starting template.")
            sys.exit(1)

        load_env_file(".env")

        dependencies = parse_deps(self.deps_file)
        for current_dep in dependencies:
            if not os.path.exists(current_dep.file_name):
                print(f"WARNING: Missing Dependency file {current_dep.file_name}. Continuing.")
                continue
            result = subprocess.run(["python3", current_dep.file_name], capture_output=True, text=True)
            print(f"executed {current_dep.file_name}:\n")
            to_open = str(current_dep.file_name).replace(self.base_path, "") + ".txt"
            with open(to_open, "r") as file:
                for line in file:
                    print(line.rstrip())
            if result.returncode != 0:
                print("finished with errors.")
                sys.exit(1)
