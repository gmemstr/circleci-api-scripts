CircleCI API Scripts
====================

**A collection of Python scripts for interacting with the CircleCI API**

These scripts can either be used individually by directly invoking them or can
be ran with the wrapper script which will eventually implement some more helpful
features. This wrapper script is written with the aim of having modules to load,
and will invoke the `RunCommand(args)` function when that module is called. See
the current scripts for examples. You can see the currently installed modules
with `./main.py modules`.

These are very generic scripts, and can be used as a baseline when developing
other tools that interact with the CircleCI API. Don't expect a configuration
file to appear anytime soon.

### How is this different from the CircleCI CLI?

The CircleCI CLI does offer a fair amount of functionality, but is aimed more 
towards things like configuration checking and Orb manipulation. This project
instead offers an easy way to fetch API endpoint data and parse it into a useful
format that can be used for local investigation. There should be little to no
overlap functionality-wise.