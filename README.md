# VPS manager

MacOS menu bar app to manage your Oracle Cloud VPS built with Python.

## Installation

1. Clone this repository:

```bash
git clone git@github.com:luccascorrea/oci-vps-manager.git
```

2. Create a virtual environment:

```bash
python3 -m venv env
```

3. Activate the virtual environment:

```bash
source env/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Create the JSON configuration file with the format below:

```json
{
    "user":"...",
    "fingerprint":"...",
    "key_file":"...",
    "tenancy":"...",
    "region":"...",
    "instance_id":"..."
}
```

6. Run the app:

```bash
python main.py
```

## Generating standalone app

1. Run the following command:

```bash
python setup.py py2app
```

> If you're using pyenv, you must install python with the `--enable-framework` flag:
    ```bash
    env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -v 3.10.0
    ```

2. An app will be generated in the `dist` folder.

3. Create master git branch:

    ```bash
    

