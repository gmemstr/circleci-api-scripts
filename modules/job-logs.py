# Useful for parsing workflow API data
# ./job-logs.py github/gmemstr/circleci-koans/1
import requests
import sys
import json
import cci


def ParseJobData(data):
    if data == {}:
        return "Not Found"
    command = final_string = ""
    template = """
=== Command ===
{command}

=== Output ===
{output}
------
    """
    for step in data['steps']:
        if step['actions'][0]['bash_command'] is not None:
            command = step['actions'][0]['bash_command']
        if 'output_url' not in step['actions'][0]:
            final_string += template.format(command=command, output="")
            continue
        url = step['actions'][0]['output_url']
        r = requests.get(url)
        data = r.json()
        output = data[0]['message']
        final_string += template.format(command=command, output=output)

    if final_string == "":
        final_string = "No logs found?"
    return final_string


def RunCommand(args):
    if cci.IsValidSlug(args[0]) is False:
        return """No project given, should be formatted as <vcs>/<org name>/<project name>/<job id>
e.g github/gmemstr/circleci-koans/1"""
    data = cci.GetData(
        "https://circleci.com/api/v1.1/project/{slug}", args[0])
    logs = ParseJobData(data)
    return logs

if __name__ == '__main__':
    logs = RunCommand(sys.argv[1:])
    print(logs)