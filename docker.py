from . import utils

def buildPush(
    _tag: str, 
    _dockerfile: str,
    _login: str, 
    _pass: str, 
    _shell: bool = True) -> None:
  utils.callThrowIfError(f"docker login -u {_login} -p {_pass}", _shell)
  try:
    utils.callThrowIfError(f"docker build --tag {_tag} -f {_dockerfile} .", _shell)
    utils.callThrowIfError(f"docker push {_tag}", _shell)
  finally:
    utils.callThrowIfError(f"docker logout", _shell)
