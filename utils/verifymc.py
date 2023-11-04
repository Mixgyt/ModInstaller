import os
import flet as ft
import utils.json_util as jsu

version = "1.17.1"
defaultPrims = f"C:\\Users\\Mix Juegos\\AppData\\Roaming\\PrismLauncher"
defaultDir = f"{jsu.ConfigReader('userPath')}\\AppData\\Roaming\\.minecraft"

def MinecraftDefaultDir():
    if(os.path.exists(defaultDir)):
        return True
    return False
    
def PrimsLauncher():   
    if(os.path.exists(defaultPrims)):
        return True
    return False