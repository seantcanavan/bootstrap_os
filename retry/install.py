import os
import re
import subprocess
import urllib.request

debug = True
reboot_required = False


def prt_plus(to_print: str):
    print(to_print + "\n")


def exec_print(command: [str], quiet: bool = None) -> int:
    output = subprocess.run(command)
    code = output.returncode
    if not quiet:
        prt_plus(f"code: {code} com: {' '.join(command)}")
    return code


def exec_strip_split(command: [str], quiet: bool = None, split_char: str = None, split_index: int = None):
    if debug:
        prt_plus(' '.join(command))
    output = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    if split_char is not None:
        output = output.split(split_char)
    if split_index is not None:
        return output[split_index]
    return output


snap_services_to_disable = [
    "snapd.service",
    "snapd.socket",
    "snapd.seeded.service",
]

prt_plus("Disabling snap services")
while len(snap_services_to_disable) > 0:
    all_running_services = exec_strip_split(["service", "--status-all"], True)
    for service in snap_services_to_disable:
        if service in all_running_services:
            if exec_print(["sudo", "systemctl", "disable", service]) == 0:
                snap_services_to_disable.remove(service)
        else:
            snap_services_to_disable.remove(service)

if os.path.exists("/usr/bin/snap"):
    prt_plus("Uninstalling all snaps")
    while True:
        installed_snaps = exec_strip_split(["snap", "list"], True, "\n")
        if len(installed_snaps) < 1 or (len(installed_snaps) == 1 and installed_snaps[0]) == '':
            prt_plus("successfully uninstalled all snaps.")
            break
        for x in range(len(installed_snaps)):
            installed_snaps[x] = installed_snaps[x].split(" ")[0]  # get just the name of the snap
        try:
            installed_snaps.remove("Name")  # remove the header row from the snap list output if it exists
        except ValueError:
            y = 2  # empty error handler
        for current_snap in installed_snaps:
            if current_snap == "":
                installed_snaps.remove("")
                continue
            exec_print(["sudo", "snap", "remove", current_snap])
            reboot_required = True
else:
    prt_plus("Snaps appear to be purged. Skipping listing them.")

if reboot_required:
    input("Please restart and run this utility again to avoid SNAP-related bugs.")
    exec_print(["sudo", "shutdown", "now"])

snap_locations = [
    '/var/lib/snapd',
    '/snap',
    '/usr/bin/snap',
]

prt_plus("Deleting leftover snap assets")
while len(snap_locations) != 0:
    for location in snap_locations:
        if not os.path.exists(location):
            snap_locations.remove(location)
        exec_print(["sudo", "rm", "-rf", location])

slack_download_url = "https://slack.com/downloads/linux"
prt_plus(f"Parsing latest slack version from {slack_download_url}")

u2 = urllib.request.urlopen(slack_download_url)
slack_regex_pattern = r'version \d\.\d\d\.\d\d'
slack_latest_version = None
slack_file_name = None

for line in u2.readlines():
    line = str(line).lower()
    matches = re.findall(slack_regex_pattern, line)
    if len(matches) == 1:
        version_number = matches[0].split(" ")
        if len(version_number) == 2:
            slack_latest_version = version_number[1]
            slack_file_name = "slack-desktop-" + slack_latest_version + "-amd64.deb"
        else:
            prt_plus(f"Got {version_number} when parsing slack download page. Expected Version X.YY.ZZZ")

apt_setup_commands = [
    # google chrome setup commands
    ["wget", "-q", "-N", "-", "https://dl-ssl.google.com/linux/linux_signing_key.pub"],
    ["sudo", "apt-key", "add", "linux_signing_key.pub"],
    ["sudo", "rm", "linux_signing_key.pub"],

    # sublime text setup commands
    ["wget", "-q", "-N", "-", "https://download.sublimetext.com/sublimehq-pub.gpg"],
    ["gpg", "--dearmor", "sublimehq-pub.gpg"],
    ["sudo", "mv", "sublimehq-pub.gpg.gpg", "/etc/apt/trusted.gpg.d/sublimehq-archive.gpg"],
    ["sudo", "rm", "sublimehq-pub.gpg"],

    # discord setup commands
    ["sudo", "-E", "gpg", "--no-default-keyring", "--keyring=/usr/share/keyrings/javinator9889-ppa-keyring.gpg",
     "--keyserver", "keyserver.ubuntu.com", "--recv-keys", "08633B4AAAEB49FC"],

    # firefox setup commands
    ["sudo", "add-apt-repository", "-y", "ppa:mozillateam/ppa"],

    # copy over static /etc/apt files
    ["sudo", "chown", "-R", "root:root", "etc/"],  # make sure root owns all files we want to copy over
    ["sudo", "cp", "-rv", "etc/", "/etc"],
]

if slack_latest_version is not None:
    print(f"slack_latest_version {slack_latest_version}")
    print(f"slack_file_name {slack_file_name}")
    apt_setup_commands.append(["wget", "-q", "-N", "-",
                               "https://downloads.slack-edge.com/releases/linux/" + slack_latest_version + "/prod/x64/" + slack_file_name])
    apt_setup_commands.append(["sudo", "dpkg", "-i", slack_file_name])
    apt_setup_commands.append(["sudo", "apt", "install", "-f"])
    apt_setup_commands.append(["sudo", "dpkg", "-i", slack_file_name])
    apt_setup_commands.append(["rm", slack_file_name])

if "VGA compatible controller: NVIDIA Corporation" in exec_strip_split(["lspci"]):
    apt_setup_commands.append(["wget", "-q", "-N", "-",
                               "https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda-repo-ubuntu2204-12-2-local_12.2.0-535.54.03-1_amd64.deb"])
    apt_setup_commands.append(
        ["sudo cp -v /var/cuda-repo-ubuntu2204-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/"])
    apt_setup_commands.append(["sudo", "dpkg", "-i", "cuda-repo-ubuntu2204-12-2-local_12.2.0-535.54.03-1_amd64.deb"])

# ubuntu update commands
apt_setup_commands.append(["sudo", "apt-get", "update", "-y", "-qq"])
apt_setup_commands.append(["sudo", "apt-get", "upgrade", "-y", "-qq"])
apt_setup_commands.append(["sudo", "apt-get", "dist-upgrade", "-y", "-qq"])
apt_setup_commands.append(["sudo", "apt-get", "autoremove", "-y", "-qq"])

os.environ["HOME"] = "/home/userwork"

prt_plus("Performing package setup commands")
for setup_command in apt_setup_commands:
    exec_print(setup_command)

apt_new_packages = [
    "build-essential",
    "cuda",
    "curl",
    "discord",
    "firefox",
    "firefox-esr",
    "font-manager",
    "git",
    "guake",
    "libfuse2",
    "pinta",
    "silversearcher-ag",
    "sublime-text",
    "ubuntu-restricted-extras",
    "google-chrome-stable"
]

prt_plus("Installing new packages")
for new_package in apt_new_packages:
    exec_print(["sudo", "apt-get", "install", "-y", new_package])
