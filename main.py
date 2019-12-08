#!/usr/bin/python3
import sys
import os
import glob
from importlib import import_module
import requests
import hashlib
import json


# Self-updater for modules
def update():
    r = requests.get(
        "https://api.github.com/repos/gmemstr/circleci-api-scripts/commits")
    data = r.json()

    file_exists = os.path.isfile("versions")

    if file_exists is False:
        with open("versions", "w+") as f:
            f.write("{}")
            print("Created versions file")

    with open("versions", "r+") as cache:
        version_cache = json.load(cache)

    if "sha" not in version_cache:
        version_cache['sha'] = ""
        version_cache['modules'] = {}

    if version_cache['sha'] != data[0]['sha']:
        # Check modules for updates
        r_mod = requests.get(
            "https://api.github.com/repos/gmemstr/circleci-api-scripts/contents/modules")
        data_mod = r_mod.json()
        for module in data_mod:
            name = module['name']
            if name not in version_cache['modules']:
                version_cache['modules'][name] = {"version": ""}
            if version_cache['modules'][name]['version'] != module['sha']:
                print("{name} updating...".format(name=name))
                r_u = requests.get(module['download_url'])
                with open("modules/" + name, "w+") as module_file:
                    module_file.write(r_u.text)
                version_cache['modules'][name]['version'] = module['sha']

    # Finally, write new versions file
    version_cache['sha'] = data[0]['sha']
    with open("versions", "w") as cache:
        json.dump(version_cache, cache, indent=4)


def get_modules():
    files = [f for f in glob.glob("modules/*.py")]
    processed_files = []

    for name in files:
        if name == "modules/__init__.py":
            continue
        f = name.replace(".py", "").replace("modules/", "")
        processed_files.append(f)

    return processed_files


# Wrapper around Python scripts to make it easier to run.
# argv index 1 is the script to run
# argv index 2 onward is passed to the runCommand
if __name__ == '__main__':
    if sys.argv[1] is None:
        print("No command given")
        exit(1)
    command = sys.argv[1].lower()
    modules = get_modules()

    # Reserved commands - ['modules']
    if command == "modules":
        for module in modules:
            print(module)
        exit()
    if command == "update":
        Update()
        exit()

    if command in modules:
        mod = import_module("modules." + command)
        result = mod.run_command(sys.argv[2:])
    else:
        result = "Command not found"

    print(result)
