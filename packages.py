import os, re
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from subprocess import call

class PkgInfo:
    def __init__(_self, _pkgZipPath: str, _annotationPath: str) -> None:
        _self.pkgZipPath = _pkgZipPath
        _self.annotationPath = _annotationPath

def callThrowIfError(_executable: str, _shell: bool = False) -> None:
    result = call(_executable, shell = _shell)
    if (result != 0):
        raise ChildProcessError(f"Command '{_executable}' returned error code '{result}'")

def adjust_annotation(_dir: str, _version: str) -> str:
    annotationFilePath = os.path.join(_dir, "annotation.json")
    print(f"Adjusting version in file '{annotationFilePath}'", flush=True)
    if (not os.path.isfile(annotationFilePath)):
        raise FileNotFoundError(f"Annotation file '{annotationFilePath}' is not found")
    content = 0
    with open(annotationFilePath, "r", encoding='utf-8') as annotationFile:
        content = annotationFile.read()
        content = re.sub(r'(999\.999\.999)', _version, content)
    if (content != 0):
        with open(annotationFilePath, "w", encoding='utf-8') as annotationFile:
            annotationFile.write(content)
    else:
        raise Exception(f"Can't adjust version in annotation file '{annotationFilePath}'")

    return annotationFilePath

def adjust_csproj(_dir: str, _version: str) -> str:
    csprojFilePath = None
    for entry in os.listdir(_dir):
        entryPath = os.path.join(_dir, entry)
        if (os.path.isfile(entryPath) and entryPath.endswith(".csproj")):
            csprojFilePath = entryPath
            break
    
    if (csprojFilePath == None):
        raise FileNotFoundError(f"Csproj file if dir '{_dir}' is not found")
    
    print(f"Adjusting version in file '{csprojFilePath}'", flush=True)
    tree = ET.parse(csprojFilePath)
    root = tree.getroot()
    for versionTag in root.iter(f"Version"):
        versionTag.text = _version
        tree.write(csprojFilePath)
        return csprojFilePath

    versionTag = ET.Element("Version")
    versionTag.text = _version
    for propertyGroupTag in root.iter(f"PropertyGroup"):
        propertyGroupTag.append(versionTag)
        tree.write(csprojFilePath)
        return csprojFilePath

    raise Exception(f"Can't adjust version in csproj file '{csprojFilePath}'")

def create_pkg(_dir: str, _version: str, _outputZipPath: str) -> PkgInfo:
    if (os.path.isfile(_outputZipPath)):
        os.remove(_outputZipPath)
    if (not os.path.isdir(_dir)):
        raise FileNotFoundError(f"Folder '{_dir}' is not a directory")

    annotationFilePath = adjust_annotation(_dir, _version)

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpDir:
        print(f"Compiling pkg '{_dir}'", flush=True)
        call(f"dotnet build \"{_dir}\" -c release -o \"{tmpDir}\"")
        print(f"Zipping pkg '{_dir}'", flush=True)
        zip_dir(tmpDir, _outputZipPath)

    return PkgInfo(_outputZipPath, annotationFilePath)

def zip_dir(_dir: str, _outputZipPath: str) -> None:
    if (os.path.isfile(_outputZipPath)):
        os.remove(_outputZipPath)
    if (not os.path.isdir(_dir)):
        raise FileNotFoundError(f"Folder '{_dir}' is not a directory")

    unneccessaryDirs = [ os.path.join(_dir, "bin"), os.path.join(_dir, "obj") ]
    for uDir in unneccessaryDirs:
        if (os.path.isdir(uDir)):
            shutil.rmtree(uDir)

    with zipfile.ZipFile(_outputZipPath, 'w', zipfile.ZIP_DEFLATED) as zipFile:
        for root, _, files in os.walk(_dir):
            for file in files:
                zipFile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), _dir))

def create_webpack(_dir: str, _outputDir: str) -> None:
    if (not os.path.isdir(_dir)):
        raise FileNotFoundError(f"Folder '{_dir}' is not a directory")
    
    distDir = os.path.join(_dir, "dist")
    if (not os.path.isdir(distDir)):
        raise FileNotFoundError(f"Can't find dist folder '{distDir}'")

    oldCwd = os.getcwd()
    os.chdir(_dir)

    print(f"Updating npm packages...", flush=True)
    callThrowIfError(f"npm i", True)

    print(f"Creating web bundle...", flush=True)
    callThrowIfError(f"npm run build", True)

    os.chdir(oldCwd)

    shutil.copytree(distDir, _outputDir, dirs_exist_ok=True)