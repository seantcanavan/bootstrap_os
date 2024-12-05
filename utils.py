import subprocess


def prt_plus(to_print: str):
    print(to_print + "\n")


def exec_print(command: [str], quiet: bool = None) -> int:
    output = subprocess.run(command)
    code = output.returncode
    if not quiet:
        prt_plus(f"code: {code} com: {' '.join(command)}")
    return code


def exec_strip_split(command: [str], quiet: bool = None, split_char: str = None, split_index: int = None):
    prt_plus(' '.join(command))
    output = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    if split_char is not None:
        output = output.split(split_char)
    if split_index is not None:
        return output[split_index]
    return output
