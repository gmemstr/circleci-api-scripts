import sys

# Wrapper around Python scripts to make it easier to run.
# argv index 1 is the script to run
# argv index 2 onward is passed to the runCommand
if __name__ == '__main__':
    if sys.argv[1] is None:
        print("No command given")
        exit(1)
    command = sys.argv[1]
    mod = __import__(command, globals(), locals(), [], 0)
    result = mod.RunCommand(sys.argv[2:])
    print(result)