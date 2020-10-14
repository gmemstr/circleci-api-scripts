import requests
import json
import yaml
from deepdiff import DeepDiff
import deepdiff

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
                final_string += f"{prefix}: orb > {v}  \n"
        elif isinstance(value, dict):
            for k, v in value.items():
                location = k.replace("root", "").replace("][", " > ").replace("[", "").replace("]", " ").replace("'", "")
                if v.get("diff"):
                    diff = v.get("diff")
                    final_string += f"{prefix}: orb > {location} \n```diff\n{diff}\n```  \n"
                else:
                    new = v.get("new_value", "")
                    old = v.get("old_value", "")
                    final_string += f"{prefix}: orb > {location}\"{old}\" -> \"{new}\"  \n"

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
