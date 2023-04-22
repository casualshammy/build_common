import os
import build_common.git as git

branch = git.get_current_branch()
commitIndex = git.get_last_commit_index()
version = f"{branch}.{commitIndex}"

github_env = os.getenv('GITHUB_ENV')
if (github_env != None):
    with open(github_env, "a") as github_env_file:
        github_env_file.write(f"tag={version}")