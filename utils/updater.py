import os
import wget
import requests



file = "ModInstaller"

def CheckVersion(version:str):
    result = False
    remote = requests.get("https://raw.githubusercontent.com/Mixgyt/ModInstaller/main/version.json")
    rversion = remote.json()

    if(version != rversion["version"]):
        print("Ultima version: "+rversion["version"])
        result = True
    return result

def UpdateVersion(newVersion:str):
    fileName = file+newVersion+".exe"
    wget.download("https://github.com/Mixgyt/ModInstaller/releases/download/"+newVersion.strip()+"/ModInstaller.exe",fileName)

def GetVersion():
    remote = requests.get("https://raw.githubusercontent.com/Mixgyt/ModInstaller/main/version.json")
    rversion = remote.json()
    return rversion["version"]
