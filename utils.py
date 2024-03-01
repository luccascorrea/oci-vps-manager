import subprocess


def copy_to_clipboard(text: str):
    process = subprocess.Popen(
        "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE
    )
    process.communicate(text.encode("utf-8"))
