import requests
import json
import yaml

# Pass in YAML dicts.
def parse_version_diff(version_latest, version_previous, parent="latest"):
    diffstring = ""
    if version_latest is None or version_previous is None:
        return ""

    for key, value in version_latest.items():
        if value is None:
            continue
        if isinstance(value, list):
            continue
        
        if isinstance(version_previous.get(key), type(value)) == False:
            if version_previous.get(key) is None:
                diffstring += "+ added {key} to {parent}\n".format(key=key, parent=parent)
                continue
            diffstring += "* changed {key} to {type} in {parent}\n".format(key=key, type=type(version_latest.get(key)).__name__, parent=parent)
            continue
        if isinstance(value, dict):
            diffstring += parse_version_diff(value, version_previous.get(key), parent +" > {}".format(key))
            continue
        if version_previous.get(key) is None:
            diffstring += "+ added {key} to {parent}\n".format(key=key, parent=parent)
        if value != version_previous.get(key):
            diffstring += "* changed {parent} > {key} from {from} to {to}".format(parent,key,version_previous.get(key), value)

    for key, value in version_previous.items():
        if isinstance(version_latest.get(key), type(value)) == False:
            if version_latest.get(key) is None:
                diffstring += "- removed {key} from {parent}\n".format(key=key, parent=parent)
                continue
            diffstring += "* changed {key} to {type} in {parent}\n".format(key=key, type=type(version_latest.get(key)).__name__, parent=parent)
            continue
        if isinstance(value, dict):
            diffstring += parse_version_diff(version_latest.get(key), value, parent +" > {}".format(key))
            continue
        if isinstance(value, list):
            continue
        if value is None:
            continue
        if version_latest.get(key) is None:
            diffstring += "- removed {key} from {parent}\n".format(key=key, parent=parent)
        if value != version_latest.get(key):
            diffstring += "* changed {parent} > {key} from {from} to {to}".format(parent,key, value, version_latest.get(key))

    return diffstring

def run_command(args):
    query = """{
      orb(name: "circleci/slack") {
        id
        versions(count: 2) {
          id
          version
          source
        }
      }
    }"""

    url = 'https://circleci.com/graphql-unstable'
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)

    latest_version = yaml.load(json_data["data"]["orb"]["versions"][0]["source"])
    previous_version = yaml.load(json_data["data"]["orb"]["versions"][1]["source"])

    diff = parse_version_diff(latest_version, previous_version)
    return diff