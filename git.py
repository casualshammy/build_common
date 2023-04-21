import subprocess

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