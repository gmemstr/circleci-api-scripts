#!/usr/bin/python3
import sys
import os
import glob
from importlib import import_module


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

    if command in modules:
        mod = import_module("modules." + command)
        result = mod.RunCommand(sys.argv[2:])
    else:
        result = "Command not found"

    print(result)