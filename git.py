import subprocess
from .utils import callThrowIfError

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

def create_tag_and_push(_tag: str, _repositorySlug: str = "origin", _userName: str | None = None) -> None:
    if (_userName != None):
        callThrowIfError(f"git config user.name \"{_userName}\"")
        callThrowIfError(f"git config user.email \"{_userName}@users.noreply.github.com\"")
    
    callThrowIfError(f"git tag -f {_tag}")
    callThrowIfError(f"git push --force origin {_tag}")

def merge(_dstBranch: str, _srcBranch: str, _push: bool = True) -> None:
    callThrowIfError(f"git checkout {_dstBranch}")
    callThrowIfError(f"git fetch")
    callThrowIfError(f"git pull")
    callThrowIfError(f"git merge {_srcBranch}")
    if (_push):
        callThrowIfError(f"git push")