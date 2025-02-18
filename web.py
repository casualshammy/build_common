import os
import shutil
import utils

def npm_build(
        _sourceDir: str, 
        _outputDir: str, 
        _buildCommand: str = "build",
        _distSubDir: str = "") -> None:
    if (not os.path.isdir(_sourceDir)):
        raise FileNotFoundError(f"Folder '{_sourceDir}' is not a directory")

    oldCwd = os.getcwd()
    os.chdir(_sourceDir)

    utils.callThrowIfError(f"npm i", True)
    utils.callThrowIfError(f"npm run {_buildCommand}", True)

    os.chdir(oldCwd)

    distDir = os.path.join(_sourceDir, "dist", _distSubDir)
    shutil.copytree(distDir, _outputDir, dirs_exist_ok=True)