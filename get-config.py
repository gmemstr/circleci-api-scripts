# Fetch configuration file from a job
# ./get-config.py github/gmemstr/circleci-koans/1
import sys
import cci


def RunCommand(args):
    if cci.IsValidSlug(args[0]) is False:
        return """No build given, should be formatted as <vcs>/<org name>/<project name>/<job id>
e.g github/gmemstr/circleci-koans/1"""

    data = cci.GetData(
        "https://circleci.com/api/v1.1/project/{slug}?view=full&circle-token={token}",
        args[0])
    return data['circle_yml']['string']


if __name__ == '__main__':
    config = RunCommand(sys.argv[1:])
    print(config)
