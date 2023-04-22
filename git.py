import subprocess, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

def get_latest_tag() -> str:
    tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'])
    tag = str(tag, encoding='utf8').strip()
    return tag

def get_current_branch() -> str:
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch = str(branch, encoding='utf8').strip()
    return branch.split("/")[-1]

def get_last_commit_index() -> int:
    index = subprocess.check_output(['git', 'rev-list', 'HEAD', '--count'])
    index = str(index, encoding='utf8').strip()
    index = int(index)
    return index

def create_tag_and_push(_userName: str, _tag: str) -> None:
    utils.callThrowIfError(f"git config user.name \"{_userName}\"")
    utils.callThrowIfError(f"git config user.email \"{_userName}@users.noreply.github.com\"")
    utils.callThrowIfError(f"git tag -f {_tag}")
    utils.callThrowIfError(f"git push --force origin {_tag}")