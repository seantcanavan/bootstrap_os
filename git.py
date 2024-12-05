from utils import exec_print


def add_git_user_and_email(username: str) -> None:
    gitconfig_file = open(f"/home/{username}/.gitconfig")
    contains_name = False
    contains_email = False
    for line in gitconfig_file:
        if line.strip().startswith("name"):
            contains_name = True
        if line.strip().startswith("email"):
            contains_email = True

    if contains_email and contains_name:
        return None

    user_name = input("Type in your git user.name: ").strip()
    user_email = input("Type in your git user.email: ").strip()

    exec_print(["git", "config", "--global", "user.name", user_name])
    exec_print(["git", "config", "--global", "user.email", user_email])


def add_git_auto_setup_remote(username: str) -> None:
    gitconfig_file = open(f"/home/{username}/.gitconfig")

    for line in gitconfig_file:
        if line.strip().startswith("autoSetupRemote"):
            return None

    exec_print(
        [
            "sudo",
            "-u",
            username,
            "git",
            "config",
            "--global",
            "--add",
            "--bool",
            "push.autoSetupRemote",
            "true",
        ]
    )
