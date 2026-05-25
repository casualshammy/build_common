from subprocess import call, check_output

def callThrowIfError(_executable: str, _shell: bool = False) -> None:
    result = call(_executable, shell = _shell)
    if (result != 0):
        raise ChildProcessError(f"Command '{_executable}' returned error code '{result}'")
    
def callWithOutput(_executable: str, _shell: bool = False) -> str:    
    result = check_output(_executable, shell=_shell)
    result = str(result, encoding='utf8').strip()
    return result
