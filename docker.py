from .utils import callThrowIfError

def buildPush(
    _tag: str, 
    _dockerfile: str,
    _login: str, 
    _pass: str, 
    _shell: bool = True) -> None:
  callThrowIfError(f"docker login -u {_login} -p {_pass}", _shell)
  try:
    callThrowIfError(f"docker build --tag {_tag} -f {_dockerfile} .", _shell)
    callThrowIfError(f"docker push {_tag}", _shell)
  finally:
    callThrowIfError(f"docker logout", _shell)
