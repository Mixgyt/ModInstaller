import requests

link = "https://bridge-mc.netlify.app/mc/server.txt"

def ServerName():
    try:
        info = requests.get(link)
        strInfo = info.text
        rangeTo = strInfo.find("-")
        return strInfo[:rangeTo]
    except:
        print("Error")
        quit()

def ServerInfo():
    try:
        info = requests.get(link)
        strInfo = info.text
        rangeFrom = strInfo.find("-")
        iServer = strInfo[rangeFrom+1:]
        allInfo = requests.get("https://api.mcsrvstat.us/3/"+iServer)
        return allInfo.json()
    except:
        print("Error")
        quit()
    