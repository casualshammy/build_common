from subprocess import call

def callThrowIfError(_executable: str, _shell: bool = False) -> None:
    result = call(_executable, shell = _shell)
    if (result != 0):
        raise ChildProcessError(f"Command '{_executable}' returned error code '{result}'")