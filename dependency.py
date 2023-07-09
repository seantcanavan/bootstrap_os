import csv
import platform as py_platform
from typing import List

import distro


class Dependency:
    def __init__(self, distro_id, distro_version, file_name, machine, name, order, system, version):
        self.distro_id = distro_id
        self.distro_version = distro_version
        self.file_name = file_name
        self.machine = machine
        self.name = name
        self.order = order
        self.system = system
        self.version = version

    def __str__(self):
        attributes = sorted(vars(self).items(), key=lambda x: x[0])  # Sort attributes alphabetically
        attr_strings = [f"{attr}: {value}" for attr, value in attributes]
        return ", ".join(attr_strings)


def build_sys_summary(system: str, machine: str, distro_id: str, distro_version: str) -> str:
    return "_".join([system, machine, distro_id, distro_version]).lower()


def build_file_name(system: str, machine: str, distro_id: str, distro_version: str, dep: str, ver: str) -> str:
    return "_".join([system, machine, distro_id, distro_version, dep, ver]).lower()


def parse_deps(input_file: str) -> List[Dependency]:
    sys_summary = build_sys_summary(py_platform.system(), py_platform.machine(), distro.id(), distro.version())
    print(f"sys_summary: {sys_summary}")

    deps: List[Dependency] = []

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            distro_id, distro_version, machine, name, order, system, version = row
            row_summary = build_sys_summary(system, machine, distro_id, distro_version)

            if row_summary != sys_summary:
                continue

            file_prefix = "/".join(input_file.split("/")[0:2]) + "/"
            file_append = build_file_name(system, machine, distro_id, distro_version, name, version) + ".py"
            file_name = file_prefix + file_append
            print(f"file_name: {file_name}")

            dependency_instance = Dependency(
                distro_id=distro_id,
                distro_version=distro_version,
                file_name=file_name,
                machine=machine,
                name=name,
                order=int(order),
                system=system,
                version=version,
            )

            deps.append(dependency_instance)
        return deps
