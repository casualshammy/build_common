import os, re
import tempfile
import zipfile
from subprocess import call

class PkgInfo:
    def __init__(_self, _pkgZipPath: str, _annotationPath: str) -> None:
        _self.pkgZipPath = _pkgZipPath
        _self.annotationPath = _annotationPath

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
        with zipfile.ZipFile(_outputZipPath, 'w', zipfile.ZIP_DEFLATED) as zipFile:
            for root, _, files in os.walk(tmpDir):
                for file in files:
                    zipFile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tmpDir))

    return PkgInfo(_outputZipPath, annotationFilePath)
        
