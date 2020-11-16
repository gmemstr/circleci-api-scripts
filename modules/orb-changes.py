import requests
import json
import yaml
from deepdiff import DeepDiff
import deepdiff
import sys
import re

def isInt(i):
    try: 
        int(i)
        return True
    except ValueError:
        return False

def normalize_string(string):
    l = string.split(" ")
    not_included = ["when", "unless", "steps", ">"]

    g = string.split(" > ")

    name = f"{g[0]}'s"
    if g[0].endswith("s"):
        name = f"{g[0][:-1]}'s"

    final = f"{g[1].title()} {name}"
    for s in l[3:]:
        if isInt(s) == False and s not in not_included:
            if s.endswith("s"):
                s = s[:-1]
            final += f" {s}"
    final = re.sub('(> ){2,}', '> ', final)
    return final

# Pass in YAML strings.
def parse_version_diff(version_latest, version_previous):
    ddiff = DeepDiff(version_latest, version_previous)
    final_string = ""

    for key, value in ddiff.items():
        prefix = "?"
        if "removed" in key:
            prefix = "Removed"
        if "added" in key:
            prefix = "Added"
        if "changed" in key or "changes" in key:
            prefix = "Changed"
        if isinstance(value, deepdiff.model.PrettyOrderedSet):
            for v in value:
                v = v.replace("root", "").replace("][", " > ").replace("[", "").replace("]", " ").replace("'", "")
                use = normalize_string(v)
                final_string += f"{prefix}: {use}  \n"
        elif isinstance(value, dict):
            for k, v in value.items():
                location = k.replace("root", "").replace("][", " > ").replace("[", "").replace("]", " ").replace("'", "")
                use = normalize_string(location)
                if isinstance(v, dict) == False:
                    final_string += f"{prefix}: {use} {v}  \n"
                    continue
                if v.get("diff"):
                    diff = v.get("diff")
                    final_string += f"{prefix}: {use} \n```diff\n{diff}\n```  \n"
                    continue
                else:
                    new = v.get("new_value", "")
                    old = v.get("old_value", "")
                    final_string += f"{prefix}: {use}\"{old}\" -> \"{new}\"  \n"

    return final_string

def run_command(args):
    if len(args) == 2:
        return (
            "A latest semver was provided, but no previous.\n"
            "Usage: ./main.py orb-changes <namespace>/<orb-name> <latest-semver> <previous-semver>"
        )
    query = """{
      orb(name: "%s") {
        id
        versions(count: 25) {
          id
          version
          source
        }
      }
    }""" % (args[0])

    url = 'https://circleci.com/graphql-unstable'
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)
    latest_version = previous_version = None
    version = ""

    if len(args) == 3:
        new = args[1]
        old = args[2]
        print(f"Comparing {new} to {old}")
        for v in json_data["data"]["orb"]["versions"]:
            if v["version"] == new:
                latest_version = yaml.load(v["source"])
                version = new
                continue
            if v["version"] == old:
                previous_version = yaml.load(v["source"])
                continue

    else:
        latest_version = yaml.load(json_data["data"]["orb"]["versions"][0]["source"])
        previous_version = yaml.load(json_data["data"]["orb"]["versions"][1]["source"])
        version = json_data["data"]["orb"]["versions"][0]["version"]

    if latest_version is None or previous_version is None:
        return (
            "Unable to find versions to compare, exiting.\n"
            "Note that for performance, we only fetch the last 25 versions."
        )

    diff = parse_version_diff(latest_version, previous_version)
    return f"## v{version}\n\n{diff}"

if __name__ == '__main__':
    result = run_command(sys.argv[1:])
    print(result)