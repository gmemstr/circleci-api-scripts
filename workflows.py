# Useful for parsing workflow API data
# ./main.py gh/gmemstr/circleci-koans
import requests
import sys
import json
import os
import cci


def ParseWorkflowData(data):
    if data == {}:
        return "Not Found"
    final_string = ""
    template = """
ID: {id}
    Status: {status}
    Duration: {duration} seconds
    Created: {created}
    Stopped: {stopped}
    Credits used: {credits}
    """
    for item in data['items']:
        proj_string = template.format(
            id=item['id'], status=item['status'], 
            duration=item['duration'], created=item['created_at'],
            stopped=item['stopped_at'], credits=item['credits_used'])
        final_string += proj_string
    if final_string == "":
        final_string = "No workflows found"
    return final_string


def RunCommand(args):
    if cci.IsValidSlug(args[0]) is False:
        return """No project given, should be formatted as <vcs>/<org name>/<project name>/<job id>
e.g github/gmemstr/circleci-koans/1"""

    data = cci.GetData(
        "https://circleci.com/api/v2/insights/{slug}/workflows/workflow?view=full&circle-token={token}",
        args[0])
    projects = ParseWorkflowData(data)
    return projects


if __name__ == '__main__':
    if cci.IsValidSlug(sys.argv[1]) is False:
        print("No project given, should be formatted as <vcs>/<org name>/<project name>")
        print("e.g gh/gmemstr/circleci-koans")
        exit()

    data = cci.GetData(
        "https://circleci.com/api/v2/insights/{slug}/workflows/workflow?view=full&circle-token={token}",
        sys.argv[1])
    projects = ParseWorkflowData(data)
    print(projects)