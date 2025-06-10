import json

def load_settings():
    current_dir = __file__.rsplit('/', 1)[0]
    with open(f"{current_dir}/config.json", "r") as f:
        return json.load(f)

settings = load_settings()
