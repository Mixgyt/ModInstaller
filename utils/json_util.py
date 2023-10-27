import json
import os

def jsonReader(fileName:str):
    data = None
    try:
        with(fileName,"r") as file:
            data = json.load(file)
    except(FileExistsError,FileNotFoundError):
        print("Error de nombre de archivo")
        return data
    
    return data