import os


def get_user_input(prompt: str) -> str:
    """Prompts the user to enter a value for the given prompt."""
    return input(prompt)


def load_env_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value
