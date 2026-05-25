import json
import urllib.request

try:
  from .utils import callThrowIfError
except ImportError:
  from utils import callThrowIfError

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

def updateDockerHubDescription(
    _dockerHubRepo: str,
    _dockerHubUsername: str,
    _dockerHubToken: str,
    _description: str,
    _shortDescription: str | None,
) -> None:
  authResp = _dockerHubRequest(
    "POST",
    "https://hub.docker.com/v2/auth/token",
    {"identifier": _dockerHubUsername, "secret": _dockerHubToken},
    {"Content-Type": "application/json"},
  )
  token = authResp["access_token"]

  patchBody: dict = {"full_description": _description}
  if _shortDescription is not None:
    patchBody["description"] = _shortDescription

  _dockerHubRequest(
    "PATCH",
    f"https://hub.docker.com/v2/repositories/{_dockerHubRepo}",
    patchBody,
    {"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
  )

def _dockerHubRequest(method: str, url: str, body: dict, headers: dict) -> dict:
  data = json.dumps(body).encode("utf-8")
  req = urllib.request.Request(url, data=data, headers=headers, method=method)
  with urllib.request.urlopen(req) as resp:
    return json.loads(resp.read().decode("utf-8"))
