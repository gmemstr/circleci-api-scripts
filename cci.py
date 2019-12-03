# Common actions for interacting with the CCI API
import requests
import json
import os

Token = os.getenv("CIRCLECI_TOKEN")


# Get data from an endpoint and return JSON dict
def GetData(endpoint, slug):
    if IsValidSlug(slug) is False:
        return {}
    url = endpoint.format(slug=slug, token=Token)
    r = requests.get(url)
    data = r.json()

    if 'message' in data.keys() and data['message'] == 'Not Found':
        return {}
    return data


# Validate project slug
def IsValidSlug(project):
    if project == "":
        return False
    decon = project.split("/")
    if len(decon) < 3:
        return False
    if len(decon[0]) == 2:
        if decon[0] != "gh" and decon[0] != "bb":
            return False
    else:
        if decon[0] != "github" and decon[0] != "bitbucket":
            return False

    return True