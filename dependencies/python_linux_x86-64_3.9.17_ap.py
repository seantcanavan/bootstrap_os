import subprocess

# Define the commands to run
commands = [
    ['sudo', 'add-apt-repository', 'ppa:deadsnakes/ppa'],
    ['sudo', 'apt-get', 'update'],
    ['sudo', 'apt-get', 'install', 'python3.9.17'],
]

# Execute each command
for command in commands:
    process = subprocess.Popen(command)
    output, error = process.communicate()

    if error is not None:
        print(f"An error occurred: {error}")
    else:
        print(f"Command '{' '.join(command)}' executed successfully")
