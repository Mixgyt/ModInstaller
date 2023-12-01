import os
import wget
import requests



file = "ModInstaller"

def CheckVersion(version:str):
    result = False
    remote = requests.get("https://raw.githubusercontent.com/Mixgyt/ModInstaller/main/version.json")
    rversion = remote.json()

    if(version != rversion["version"]):
        UpdateVersion(rversion["version"])
        result = True
    return result

def UpdateVersion(newVersion:str):
    fileName = file+newVersion+".exe"
    wget.download("https://github.com/Mixgyt/ModInstaller/releases/download/"+newVersion.strip()+"/ModInstaller.exe",fileName)

if __name__ == "__main__":
    import json_util as jsu
    remote = requests.get("https://raw.githubusercontent.com/Mixgyt/ModInstaller/main/version.json")
    rversion = remote.json()
    vnewversion = rversion["version"].replace("v","")
    vnenum = float(vnewversion)

    version = jsu.ConfigReader("version")
    vversion = version.replace("v","")
    vnum = float(vversion)
    
    if(vnum < vnenum):
        os.remove("ModInstaller"+version+".exe")
        "Eliminado"
