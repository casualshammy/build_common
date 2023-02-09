import subprocess

def get_latest_tag() -> str:
    tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'])
    tag = str(tag, encoding='utf8').strip()
    return tag