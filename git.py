import subprocess
from . import utils

def get_latest_tag() -> str:
    tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'])
    tag = str(tag, encoding='utf8').strip()
    return tag

def get_version_from_current_branch() -> str:
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch = str(branch, encoding='utf8').strip()
    return branch.split("/")[-1]
    
def get_current_branch_name() -> str:
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch = str(branch, encoding='utf8').strip()
    return branch

def get_last_commit_index() -> int:
    index = subprocess.check_output(['git', 'rev-list', 'HEAD', '--count'])
    index = str(index, encoding='utf8').strip()
    index = int(index)
    return index

def create_tag_and_push(_tag: str, _repositorySlug: str = "origin", _userName: str | None = None, _shell: bool = False) -> None:
    if (_userName != None):
        utils.callThrowIfError(f"git config user.name \"{_userName}\"", _shell)
        utils.callThrowIfError(f"git config user.email \"{_userName}@users.noreply.github.com\"", _shell)
    
    utils.callThrowIfError(f"git tag -f {_tag}", _shell)
    utils.callThrowIfError(f"git push --force origin {_tag}", _shell)

def merge(_dstBranch: str, _srcBranch: str, _push: bool = True, _userName: str | None = None, _shell: bool = False) -> None:
    if (_userName != None):
        utils.callThrowIfError(f"git config user.name \"{_userName}\"", _shell)
        utils.callThrowIfError(f"git config user.email \"{_userName}@users.noreply.github.com\"", _shell)
        
    utils.callThrowIfError(f"git checkout {_dstBranch}", _shell)
    utils.callThrowIfError(f"git fetch", _shell)
    utils.callThrowIfError(f"git pull", _shell)
    utils.callThrowIfError(f"git merge {_srcBranch}", _shell)
    if (_push):
        utils.callThrowIfError(f"git push", _shell)
        
    utils.callThrowIfError(f"git checkout {_srcBranch}", _shell)