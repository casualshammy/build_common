import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import git

branch = git.get_current_branch()
commitIndex = git.get_last_commit_index()
version = f"{branch}.{commitIndex}"

github_env = os.getenv('GITHUB_ENV')
if (github_env != None):
    with open(github_env, "a") as github_env_file:
        github_env_file.write(f"tag={version}")
        print(f"Set env var to github: tag={version}", flush= True)