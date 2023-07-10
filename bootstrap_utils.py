import subprocess


def get_user_input(prompt: str) -> str:
    """Prompts the user to enter a value for the given prompt."""
    return input(prompt)


def load_env_file(file_path):
    command = [
        "/bin/bash",
        "source",
        file_path,
    ]
    process = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    print(process)
