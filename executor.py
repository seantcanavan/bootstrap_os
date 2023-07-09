import os
import subprocess
from pprint import pprint

from dependency import parse_deps


class Executor:
    def __init__(self, debug: bool, deps_file: str):
        self.debug = debug
        self.deps_file = deps_file

        dependencies = parse_deps(self.deps_file)
        for current_dep in dependencies:
            if not os.path.exists(current_dep.file_name):
                print(f"WARNING: Missing Dependency file {current_dep.file_name}. Continuing.")
                continue
            try:  # Open a command line and execute the command specified by source_url
                output = subprocess.run(["python3", current_dep.file_name], capture_output=True, text=True).stdout.strip()
                print(f"Successfully ran dep file {current_dep.file_name}")
                if self.debug:
                    pprint(output)
            except subprocess.CalledProcessError as e:
                print(f"Installation failed. Error: {e}")
