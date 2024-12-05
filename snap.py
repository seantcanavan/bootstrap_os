import os

from utils import exec_print, exec_strip_split, prt_plus


def remove_snap_services() -> None:
    prt_plus("Disabling snap services")
    snap_services_to_disable = [
        "snapd.service",
        "snapd.socket",
        "snapd.seeded.service",
    ]
    reboot_required = False
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
            if (
                len(installed_snaps) < 1
                or (len(installed_snaps) == 1 and installed_snaps[0]) == ""
            ):
                prt_plus("successfully uninstalled all snaps.")
                break
            for x in range(len(installed_snaps)):
                installed_snaps[x] = installed_snaps[x].split(" ")[
                    0
                ]  # get just the name of the snap
            try:
                installed_snaps.remove(
                    "Name"
                )  # remove the header row from the snap list output if it exists
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
        exec_print(["sudo", "reboot", "now"])


def remove_snap_folders(username: str) -> None:
    snap_locations = [
        "/snap",
        "/usr/bin/snap",
        "/usr/lib/snapd",
        "/var/cache/snapd",
        "/var/lib/snapd",
        "/var/snap",
        f"/home/{username}/snap",
    ]

    prt_plus("Deleting leftover snap assets")
    while len(snap_locations) != 0:
        for location in snap_locations:
            if not os.path.exists(location):
                snap_locations.remove(location)
            exec_print(["sudo", "rm", "-rf", location])
