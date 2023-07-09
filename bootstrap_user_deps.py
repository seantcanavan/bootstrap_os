import os
import sys

from executor import Executor

if os.geteuid() == 0:
    print("This script DOES NOT REQUIRE sudo to run. DO NOT RUN IT WITH SUDO. EVER. THAT WOULD BE BAD.")
    sys.exit(1)

Executor(True, 'dependencies/user/deps.csv')
