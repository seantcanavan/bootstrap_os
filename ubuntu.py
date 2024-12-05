import os

from git import add_git_auto_setup_remote, add_git_user_and_email
from install_slack import download_slack_deb
from install_ungoogled_chromium import download_ungoogled_chromium_deb
from snap import remove_snap_services, remove_snap_folders
from utils import exec_print, exec_strip_split, prt_plus

logged_in_user = exec_strip_split(["whoami"])

add_git_user_and_email(username=logged_in_user)
add_git_auto_setup_remote(username=logged_in_user)
# remove_snap_services()
# remove_snap_folders(username=logged_in_user)

apt_setup_commands = [
    ["wget", "-N", "https://download.sublimetext.com/sublimehq-pub.gpg"],
    ["gpg", "--dearmor", "sublimehq-pub.gpg"],
    [
        "sudo",
        "mv",
        "sublimehq-pub.gpg.gpg",
        "/etc/apt/trusted.gpg.d/sublimehq-archive.gpg",
    ],
    ["sudo", "rm", "sublimehq-pub.gpg"],
    [
        "sudo",
        "-E",
        "gpg",
        "--no-default-keyring",
        "--keyring=/usr/share/keyrings/javinator9889-ppa-keyring.gpg",
        "--keyserver",
        "keyserver.ubuntu.com",
        "--recv-keys",
        "08633B4AAAEB49FC",
    ],
    ["sudo", "add-apt-repository", "-y", "ppa:mozillateam/ppa"],
    [
        "sudo",
        "chown",
        "-R",
        "root:root",
        "etc/",
    ],
    ["sudo", "cp", "-rv", "etc/", "/etc"],
    ["sudo", "apt-get", "update", "-y", "-qq"],
    ["sudo", "apt-get", "upgrade", "-y", "-qq"],
    ["sudo", "apt-get", "dist-upgrade", "-y", "-qq"],
    ["sudo", "apt-get", "autoremove", "-y", "-qq"],
]

apt_setup_commands.extend(download_ungoogled_chromium_deb())
print("about to call")
apt_setup_commands.extend(download_slack_deb())


# ubuntu update commands
os.environ["HOME"] = "/home/" + logged_in_user

prt_plus("Performing package setup commands")
for setup_command in apt_setup_commands:
    exec_print(setup_command)

apt_new_packages = [
    "btop",
    "build-essential",
    "curl",
    "discord",
    "firefox",
    "firefox-esr",
    "font-manager",
    "git",
    "google-chrome-stable",
    "guake",
    "htop",
    "libfuse2",
    "pinta",
    "python3-venv",
    "silversearcher-ag",
    "sublime-text",
    "ubuntu-restricted-extras",
]

prt_plus("Installing new packages")
for new_package in apt_new_packages:
    exec_print(["sudo", "apt-get", "install", "-y", new_package])

prt_plus("Setting up Git")
ssh_priv_file = "/home/" + logged_in_user + "/.ssh/id_rsa"
ssh_pub_file = "/home/" + logged_in_user + "/.ssh/id_rsa.pub"


if os.path.exists(ssh_priv_file):
    exec_print(
        [
            "sudo",
            "-u",
            logged_in_user,
            "ssh-keygen",
            "-t",
            "rsa",
            "-b",
            "4096",
            "-f",
            ssh_priv_file,
            '-N ""',
        ]
    )

exec_print(["cat", ssh_pub_file])
input("Your ssh public key was just printed. Copy it to github and press enter when done.").strip()

github_username = input("Enter your github username: ")
github_pat = input("Enter your github PAT. This will be used to unlock calls to private repos. ")
exec_print(
    [
        "sudo",
        "-u",
        logged_in_user,
        "git",
        "config",
        "--global",
        "url.https://{0}:{1}@github.com.insteadOf".format(github_username, github_pat),
        "https://github.com",
    ]
)


if user_email not in exec_strip_split(["sudo", "-u", logged_in_user, "gpg", "--list-keys", "--with-colons"]):
    print(f"No GPG key found for email {user_email}. Creating one now.")
    gpg_file_lines = [
        "Key-Type: RSA",
        "Key-Length: 4096",
        f"Name-Real: {user_name}",
        f"Name-Email: {user_email}",
        "Expire-Date: 1y",
    ]

    passphrase = input("Enter your passphrase for the gpg key")

    gpg_file_lines.append("Passphrase: " + passphrase)
    gpg_file_lines.append("%commit")
    gpg_file_lines.append("%echo done")

    gpg_file_name = "gpg_config_file"

    with open("gpg_config_file", "w") as gpg_config_file:
        gpg_config_file.writelines([line + "\n" for line in gpg_file_lines])

    exec_print(["sudo", "-u", logged_in_user, "gpg", "--gen-key", "--batch", gpg_file_name])

exec_print(["sudo", "-u", logged_in_user, "gpg", "--armor", "--export", user_email])
print("Your GPG key has been printed. Paste it into github and hit enter to continue.")
