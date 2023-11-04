import json
import os

def jsonReader(fileName:str):
    fileName = fileName.strip()
    fileName += ".json"
    data = None
    try:
        with open(fileName,"r") as file:
            data = json.load(file)
            
    except(FileExistsError,FileNotFoundError):
        print("Error de nombre de archivo")
    
    return data

def ConfigReader(config:str):
    data = None
    try:
        with open("settings.json","r") as file:
            arch = json.load(file)
            data = arch[config]
    except(KeyError, FileExistsError, FileNotFoundError):
        print("Error de lectura")
        data = None

    return data


def ConfigEdit(config:str,value):
    fileName = "settings.json"
    data = {}
    try:
        with open(fileName,"r") as file:
            data = json.load(file)
        data[config] = value
        with open(fileName,"w") as file:
            json.dump(data,file,indent="\t")

    except():
        print("Error al modificar archivo")
        return False
    
    return data

def ConfigCreate():
    fileName = "settings.json"
    data = {}
    data["userPath"] = f"C:{os.environ.get('HOMEPATH')}"
    try:
        with open(fileName,"w") as file:
            json.dump(data,file,indent="\t")
            
    except():
        print("Error al crear json")
        return False
    
    return True

def jsonRemove(fileName:str):
    fileName = fileName.strip()
    fileName += ".json"
    try:
        os.remove(f"./{fileName}")

    except(FileExistsError,FileNotFoundError):
        print("Error archivo no encontrado")
        return False
    
    return True