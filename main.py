import sys
import os
import glob

# Wrapper around Python scripts to make it easier to run.
# argv index 1 is the script to run
# argv index 2 onward is passed to the runCommand
if __name__ == '__main__':
    if sys.argv[1] is None:
        print("No command given")
        exit(1)
    command = sys.argv[1].lower()

    # Reserved commands - ['modules']
    if command == "modules":
        files = [f for f in glob.glob("*.py")]

        for f in files:
            f = f.replace(".py", "")
            # Known files that we shouldn't bother listing.
            if f == "main" or f == "cci":
                continue
            print(f)
        exit()

    mod = __import__(command, globals(), locals(), [], 0)
    result = mod.RunCommand(sys.argv[2:])
    print(result)