import os
import xml.etree.ElementTree as ET
from subprocess import call

def GetProjectPaths(_dir: str) -> dict[str, str]:
    result = {}
    for root, dirs, files in os.walk(_dir):
        for file in files:
            if (file.endswith(".csproj")):
                result[root] = os.path.join(root, file)
    return result

def GetPackableProjects(_csprojFilePaths: list[str]) -> list[str]:
    result = []
    for path in _csprojFilePaths:
        tree = ET.parse(path)
        root = tree.getroot()
        for isPackableTag in root.iter(f"IsPackable"):
            if (isPackableTag.text == "true"):
                result.append(path)
                break
    return result

def BuildPackNugets(_tag: str, _nugetsDir: str, _csprojFilePaths: list[str]) -> None:
    for csprojPath in _csprojFilePaths:
        dir = os.path.dirname(csprojPath)
        call(f"dotnet pack \"{dir}\" -c Release /p:Version={_tag} -o {_nugetsDir}", shell=True)

def PackAllNugetsInDir(_tag: str, _nugetsDir: str, _dir: str = None) -> None:
    if (_dir == None):
        _dir = os.getcwd()

    print(f"=========================================================", flush=True)
    print(f"Working dir: {_dir}", flush=True)
    print(f"Nugets dir: {_nugetsDir}", flush=True)
    print(f"Tag: {_tag}", flush=True)
    print(f"=========================================================", flush=True)

    allProjects = GetProjectPaths(_dir)
    packableProjects = GetPackableProjects(allProjects.values())
    for csprojPath in packableProjects:
        print(f"Found packable project: '{csprojPath}'", flush=True)

    BuildPackNugets(_tag, _nugetsDir, packableProjects)

def PushAllNugetsInDir(_nugetsDir: str, _apiKey: str, _source: str = None) -> None:
    if (_source == None):
        _source = "https://api.nuget.org/v3/index.json"
    for entryName in os.listdir(_nugetsDir):
        fullPath = os.path.join(_nugetsDir, entryName)
        if (os.path.isfile(fullPath) and entryName.endswith(".nupkg")):
            print(f"Pushing nuget pkg: '{fullPath}'", flush=True)
            call(f"dotnet nuget push \"{fullPath}\" --api-key {_apiKey} --source {_source}", shell=True)

# tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'])
# tag = str(tag, encoding='utf8').strip()
# dir = os.path.join(os.getcwd(), "nugets")
# PackAllNugetsInDir(tag, dir)
# PushAllNugetsInDir(dir, "api-key")