import sys
import cci
import subprocess

def determine_provider(s):
	if "github.com" in s:
		return "gh"
	if "bitbucket.com" in s:
		return "bb"

def get_git_info():
	branch = subprocess.check_output(["git", "branch", "--show-current"]).strip().decode("utf-8")
	remote = subprocess.check_output(["git", "remote", "get-url", "origin"]).strip().decode("utf-8")
	provider = determine_provider(remote)
	project_name = remote.split(":")[-1].replace(".git", "")
	return {"branch": branch, "remote": remote, "provider": provider, "project": project_name}

def run_command(args):
	git_data = get_git_info()
	slug = git_data.get("provider") + "/" + git_data.get("project")
	return cci.post_data("https://circleci.com/api/v2/project/{slug}/pipeline", slug, {"branch": git_data.get("branch")})

if __name__ == '__main__':
    result = RunCommand(sys.argv[1:])
    print(result)
