CircleCI API Scripts
====================

**A collection of Python (3) scripts for interacting with the CircleCI API**

[![CircleCI](https://circleci.com/gh/gmemstr/circleci-api-scripts/tree/master.svg?style=svg)](https://circleci.com/gh/gmemstr/circleci-api-scripts/tree/master)

These scripts can either be used individually by directly invoking them or can
be ran with the wrapper script which will eventually implement some more helpful
features. This wrapper script is written with the aim of having modules to load,
and will invoke the `run_command(args)` function when that module is called. See
the current scripts for examples. You can see the currently installed modules
with `./main.py modules`.

These are very generic scripts, and can be used as a baseline when developing
other tools that interact with the CircleCI API. Don't expect a configuration
file to appear anytime soon.

You'll need to set your [CircleCI API token](https://circleci.com/account/api)
with `export CIRCLECI_TOKEN=<token>` for this tool to work.

### Writing your own module

Writing your own module is relatively straightforward. Each one should implement
a function that will be intially called by the main script, named `run_command`,
and should accept a list of args. e.g

```python
def run_command(args):
    print(args)
    return "done!"
```

This is expected to return a string, which will be printed as a result for the
user. This also makes it very easy to allow calling of the script on it's own by
implementing the following code block:

```python
if __name__ == '__main__':
    result = run_command(sys.argv[1:])
    print(result)
```

A few helper functions are available, which are common functions scripts 
typically have to call. The most important of which is 
`get_data(endpoint, slug)`, which will fetch the data from the endpoint 
requested and handle any errors that arise from the request. There is also a 
`post_data(endpoint, slug, data)` function for POST requests. The endpoint 
should be formatted like so:

```
https://circleci.com/api/<endpoint>/{slug}
```

where `{slug}` will be replaced with the project slug 
(`:vcs/:username/:project`) provided by the user.

Besides that, take a look at the existing modules, and have fun! As a 
"best-practice" note, modules should aim to implement features using no, or very
few, additional Python package requirements.

### How is this different from the CircleCI CLI?

The CircleCI CLI does offer a fair amount of functionality, but is aimed more 
towards things like configuration checking and Orb manipulation. This project
instead offers an easy way to fetch API endpoint data and parse it into a useful
format that can be used for local investigation. There should be little to no
overlap functionality-wise.