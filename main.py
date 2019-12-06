#!/usr/bin/python3
import sys
import os
import glob
from importlib import import_module
import requests
import hashlib
import json


# Self-updater
# Abandon hope, all ye who enter (it's not that bad)
def Update():
    r = requests.get("https://api.github.com/repos/gmemstr/circleci-api-scripts/commits")
    data = r.json()

    with open("versions") as cache:
        version_cache = json.load(cache)
    # We need to update something, but what?
    if "sha" not in version_cache:
        version_cache['sha'] = ""
        version_cache['modules'] = {}
    if version_cache['sha'] != data[0]['sha']:
        # Check modules for updates
        r_mod = requests.get("https://api.github.com/repos/gmemstr/circleci-api-scripts/contents/modules")
        data_mod = r_mod.json()
        for module in data_mod:
            name = module['name']
            if name not in version_cache['modules']:
                version_cache['modules'][name] = {"version": ""}
            if version_cache['modules'][name]['version'] != module['sha']:
                print("{name} updating...".format(name=name))
                r_u = requests.get(module['download_url'])
                f = open("modules/" + name, "w+")
                f.write(r_u.text)
                f.close()
                version_cache['modules'][name]['version'] = module['sha']
    # Finally, write new version file
    version_cache['sha'] = data[0]['sha']
    with open("versions", "w") as cache:
        json.dump(version_cache, cache, indent=4)

def GetModules(): 
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
    modules = GetModules()

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
        result = mod.RunCommand(sys.argv[2:])
    else:
        result = "Command not found"

    print(result)