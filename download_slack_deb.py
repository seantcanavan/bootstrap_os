import re
import urllib.request
from typing import List
from urllib.parse import urlparse
from utils import prt_plus


def download_slack_deb(username: str) -> List[List[str]]:
    print("download_slack_deb")
    slack_download_url = "https://slack.com/downloads/instructions/linux?ddl=1&build=deb"

    prt_plus(f"Parsing latest slack version from {slack_download_url}")

    slack_html = urllib.request.urlopen(slack_download_url)
    slack_regex_pattern = r"https:\/\/downloads\.slack-edge\.com\/desktop-releases\/linux\/x64\/\d+\.\d+\.\d+\/slack-desktop-\d+\.\d+\.\d+-amd64\.deb"
    slack_download_url = None

    for x, line in enumerate(slack_html.readlines()):
        line = line.decode("utf-8").strip().lower()
        if line.count("desktop-releases/linux/x64") > 0:
            line_parts = line.split("\n")
            for line_part in line_parts:
                matches = re.findall(slack_regex_pattern, line_part)
                if len(matches) > 0:
                    slack_download_url = matches[0]

    slack_setup_commands: List[List[str]] = []

    if slack_download_url is not None:
        slack_file_name = urlparse(slack_download_url).path.split("/")[-1]
        print(f"slack_download_url {slack_download_url}")
        print(f"slack_file_name {slack_file_name}")
        slack_setup_commands.append(["sudo", "-u", username, "wget", "-N", slack_download_url])
        slack_setup_commands.append(["sudo", "dpkg", "-i", slack_file_name])
        slack_setup_commands.append(["sudo", "apt", "install", "-f"])
        slack_setup_commands.append(["sudo", "dpkg", "-i", slack_file_name])

    return slack_setup_commands
