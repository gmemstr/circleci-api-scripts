import sys
import cci

# Duplication to check:
# Similar job names (suggesting reuse)
# Duplicate remote_docker entries

# Parse results to templates.
def parse_results(results):
    fstring = ""
    template_unique_commands = """
{command}
----> called {count}x
----> {appears_in}
"""
    joiner = ", "
    for not_unique in results['not_unique']:
        if results['not_unique'][not_unique]['count'] == 1:
            continue
        fstring += template_unique_commands.format(
            command=not_unique,
            count=results['not_unique'][not_unique]['count'],
            appears_in=joiner.join(
                results['not_unique'][not_unique]['jobs']))

    return fstring

# Duplicated steps between jobs.
def dupe_steps(jobs):
    unique_steps = []
    not_unique = {}

    for job in jobs:
        job_values = jobs[job]
        for step in job_values['steps']:
            if isinstance(step, str):
                step = step
            if isinstance(step, dict):
                step = (step['run']['command'])
            # Ignore checkout command, since that's bound to be duplicate.
            if step == "checkout":
                continue
            if step not in unique_steps:
                if step not in not_unique:
                    not_unique[step] = {"count": 1, "jobs": [job]}
                unique_steps.append(step)
            else:
                not_unique[step]['count'] += 1
                not_unique[step]['jobs'].append(job)

    return not_unique


def run_command(args):
    config_file = None
    with open(args[0], 'r') as stream:
        config_file = cci.parse_config(stream)

    dupes = dupe_steps(config_file['jobs'])
    res = parse_results({"not_unique": dupes})
    return res
