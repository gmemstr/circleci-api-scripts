# Fetch configuration file from a job
import sys
import cci


def run_command(args):
    if cci.is_valid_slug(args[0]) is False:
        return """No build given, should be formatted as <vcs>/<org name>/<project name>/<job id>
e.g github/gmemstr/circleci-koans/1"""

    data = cci.get_data(
        "https://circleci.com/api/v1.1/project/{slug}",
        args[0])

    return data['circle_yml']['string']


if __name__ == '__main__':
    config = run_command(sys.argv[1:])
    print(config)
