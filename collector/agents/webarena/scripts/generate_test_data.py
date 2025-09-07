"""Replace the website placeholders with website domains from env_config
Generate the test data"""
import json

from browser_env.env_config import *


def main() -> None:
    with open("config_files/test.raw.json", "r") as f:
        raw = f.read()
    raw = raw.replace("__SHOPPING__", SHOPPING)
    raw = raw.replace("__HEALTH__", HEALTH)
    raw = raw.replace("__NEWS__", NEWS)
    raw = raw.replace("__LINKEDIN__", LINKEDIN)
    raw = raw.replace("__SPOTIFY__", SPOTIFY)
    raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)
    with open("config_files/test.json", "w") as f:
        f.write(raw)
    # split to multiple files
    data = json.loads(raw)
    for idx, item in enumerate(data):
        with open(f"config_files/{idx}.json", "w") as f:
            json.dump(item, f, indent=2)


if __name__ == "__main__":
    main()
