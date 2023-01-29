from setuptools import setup

APP = ["main.py"]
DATA_FILES = ["config.json"]
OPTIONS = {
    "argv_emulation": True,
    "plist": {
        "LSUIElement": True,
    },
    "packages": ["rumps", "oci"],
    "includes": ["cryptography", "cffi"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
