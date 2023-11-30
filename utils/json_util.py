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
            try:
                print("Error de lectura, se ha creado un nuevo archivo de configuraciones")
                arch = ConfigCreate()
                data = arch[config]
            except(KeyError):
                data = ConfigAdd(config,"")
                data = data[config]
                print("Se ha creado la key faltante")

    return data


def ConfigAdd(config:str,value):
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

        with open("settings.json","r") as file:
            arch = json.load(file)
            data = arch
    except():
        print("Error al crear json")
        data = None
        return data
    
    return data

def jsonRemove(fileName:str):
    fileName = fileName.strip()
    fileName += ".json"
    try:
        os.remove(f"./{fileName}")

    except(FileExistsError,FileNotFoundError):
        print("Error archivo no encontrado")
        return False
    
    return True