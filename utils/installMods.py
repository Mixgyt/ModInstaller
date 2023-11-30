import os
import zipfile
import shutil
import wget

link = "https://bridge-mc.netlify.app/mc/mods.txt"
archivo_local = "link.txt"
nombre_mods = "mods.zip"

def InstallMods(path:str,deleteOld:bool):
    result = bool
    link_mods = str
    wget.download(link,archivo_local)

    with open(archivo_local,"r") as file:
        for linea in file:
            link_mods = linea.strip()
    os.remove(archivo_local)
    wget.download(link_mods,nombre_mods)

    mods = zipfile.ZipFile(nombre_mods,"r")
    
    if(os.path.isdir(path) and deleteOld):
        shutil.rmtree(path)
        os.mkdir(path)
        mods.extractall(path)
        result = True
    elif (os.path.isdir(path)):
        mods.extractall(path)
        result = True
    else:
        print("Error no se ecuentra el directorio")
        result = False

    mods.close()
    os.remove(nombre_mods)
    return result
