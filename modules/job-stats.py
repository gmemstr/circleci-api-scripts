# Collect and calculate job stats and percentages.
import cci


# Format collected job stats into their own strings
def format_job_data(stats, count):
    result = {"why": "", "outcomes": "", "statuses": ""}
    tmpl = "{string} {perc} "

    for w in stats["why"].keys():
        result["why"] += tmpl.format(string=w,
                                     perc=str(round(stats["why"][w] / count * 100)) + "%")

    for w in stats["outcomes"].keys():
        result["outcomes"] += tmpl.format(string=w,
                                          perc=str(round(stats["outcomes"][w] / count * 100)) + "%")

    for w in stats["statuses"].keys():
        result["statuses"] += tmpl.format(string=w,
                                          perc=str(round(stats["statuses"][w] / count * 100)) + "%")

    return result


# Parse job data into usable format dict and return formatted template.
def parse_job_data(data):
    template = """
Job summary (last {count} jobs)
---
Launch reason: {why}
Avg. build time: {build_time}
Outcomes: {outcomes}
Status: {statuses}
"""
    stats = {"why": {}, "build_time_total": 0, "outcomes": {}, "statuses": {}}
    total_jobs = len(data)
    for job in data:
        # Why job failed
        if job["why"] not in stats["why"]:
            stats["why"][job["why"]] = 0
        stats["why"][job["why"]] = stats["why"][job["why"]] + 1

        # Outcomes of jobs
        if job["outcome"] not in stats["outcomes"]:
            stats["outcomes"][job["outcome"]] = 0
        stats["outcomes"][job["outcome"]] = stats["outcomes"][job["outcome"]] + 1

        # Status of jobs
        if job["status"] not in stats["statuses"]:
            stats["statuses"][job["status"]] = 0
        stats["statuses"][job["status"]] = stats["statuses"][job["status"]] + 1

        if job["build_time_millis"] is not None:
            stats["build_time_total"] += job["build_time_millis"]
    stats["build_time_total"] = str(
        round(stats["build_time_total"] / 1000 / total_jobs)) + "s"
    formatted_data = format_job_data(stats, total_jobs)

    return template.format(
        count=total_jobs,
        why=formatted_data["why"],
        build_time=stats["build_time_total"],
        outcomes=formatted_data["outcomes"],
        statuses=formatted_data["statuses"])


def run_command(args):
    if cci.is_valid_slug(args[0]) is False:
        return """No project given, should be formatted as <vcs>/<org name>/<project name>
e.g gh/gmemstr/circleci-koans"""
    url = "https://circleci.com/api/v1.1/project/{slug}?limit=100&shallow=true"
    if len(args) > 1:
        url = "https://circleci.com/api/v1.1/project/{slug}?limit=" + \
            args[1] + "&shallow=true"

    data = cci.get_data(
        url,
        args[0])
    stats = parse_job_data(data)
    return stats


if __name__ == '__main__':
    stats = run_command(sys.argv[1:])
    print(stats)
