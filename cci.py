# Common actions for interacting with the CCI API
import requests
import json
import os

Token = os.getenv("CIRCLECI_TOKEN")


# Get data from an endpoint and return JSON dict, auto inject token
def get_data(endpoint, slug=""):
    if slug != "" and is_valid_slug(slug) is False:
        return {}
    url = endpoint.format(slug=slug)
    r = requests.get(
        url,
        params={
            "circle-token": Token},
        headers={
            "Accept": "application/json"})
    data = r.json()

    if 'message' in data.keys() and data['message'] == 'Not Found':
        return {}
    return data


# Post dict to endpoint, automatically inject token
def post_data(endpoint, slug="", data={}):
    if slug != "" and is_valid_slug(slug) is False:
        return {}
    url = endpoint.format(slug=slug)
    r = requests.post(
        url,
        data=data,
        params={
            "circle-token": Token},
        headers={
            "Accept": "application/json"})
    data = r.json()

    if 'message' in data.keys() and data['message'] == 'Not Found':
        return {}
    return data


# Validate project slug
def is_valid_slug(project):
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


# Validate API/token setup.
def validate_setup():
    if Token is None or Token == "":
        return "token unset"

    logged_in = get_data("https://circleci.com/api/v1.1/me")
    if 'message' in logged_in and logged_in['message'] == "You must log in first.":
        return "cannot authenticate with api"

    return True
