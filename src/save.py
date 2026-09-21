import os
import json

def getPathToSave(saveslot):
    return f"../saves/{saveslot}.json"

def saveData(saveslot,data):
    os.makedirs("../saves/",exist_ok=True)
    with open(getPathToSave(saveslot),"w") as f:
        json.dump(data,f)

def loadData(saveslot):
    path=getPathToSave(saveslot)
    if (os.path.isfile(path)):
        with open(path,"r") as f:
            return json.load(f)
    else:
        return False # does not exist