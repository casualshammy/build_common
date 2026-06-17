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

def buildPushMultiArch(
    _tags: list[str], 
    _dockerfile: str,
    _login: str, 
    _pass: str, 
    _platforms: list[str] | None = None,
    _cacheFrom: list[str] | None = None,
    _cacheTo: list[str] | None = None) -> None:
  callThrowIfError(f"docker login -u {_login} -p {_pass}", True)
  try:
    platforms = ",".join(_platforms or ["linux/amd64", "linux/arm64"])
    tags = " ".join([f"--tag {t}" for t in _tags])
    cacheFrom = " ".join([f"--cache-from {c}" for c in (_cacheFrom or [])])
    cacheTo = " ".join([f"--cache-to {c}" for c in (_cacheTo or [])])
    callThrowIfError(f"docker buildx build --platform {platforms} {tags} -f {_dockerfile} {cacheFrom} {cacheTo} --push .", True)
  finally:
    callThrowIfError(f"docker logout", True)

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
