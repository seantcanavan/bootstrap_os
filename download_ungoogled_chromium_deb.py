import re
import urllib.request
from typing import List

from utils import prt_plus


def download_ungoogled_chromium_deb() -> List[List[str]]:
    ungoogled_chromium_url = (
        "https://software.opensuse.org//download.html?project=home%3Aungoogled_chromium&package=ungoogled-chromium"
    )
    prt_plus(f"Parsing latest Ungoogled Chromium version from {ungoogled_chromium_url}")

    ungoogled_chromium_html = urllib.request.urlopen(ungoogled_chromium_url)
    ungoogled_chromium_regex_pattern = r"https:\/\/download\.opensuse\.org\/repositories\/home:\/ungoogled_chromium\/ubuntu_lunar\/amd64\/ungoogled-chromium_\d+\.\d+\.\d+\.\d+-\d+_amd64\.deb"
    ungoogled_chromium_file_name = None

    for line in ungoogled_chromium_html.readlines():
        line = line.decode("utf-8").strip().lower()
        matches = re.findall(ungoogled_chromium_regex_pattern, line)
        if len(matches) == 1:
            ungoogled_chromium_file_name = matches[0]
            break

    ungoogled_chromium_setup_commands: List[List[str]] = []

    if ungoogled_chromium_file_name is not None:
        print(f"ungoogled_chromium_file_name {ungoogled_chromium_file_name}")
        ungoogled_chromium_setup_commands.append(["wget", "-N", ungoogled_chromium_file_name])
        ungoogled_chromium_setup_commands.append(["sudo", "dpkg", "-i", ungoogled_chromium_file_name])
        ungoogled_chromium_setup_commands.append(["sudo", "apt", "install", "-f"])
        ungoogled_chromium_setup_commands.append(["sudo", "dpkg", "-i", ungoogled_chromium_file_name])

    return ungoogled_chromium_setup_commands
