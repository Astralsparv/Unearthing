from random import randrange as randfloat

def give_item(player,item,count):
    if (item in player["inventory"]):
        player["inventory"][item]+=count
    else:
        player["inventory"][item]=count

def give_loot_table(player,table):
    given={}
    for i,obj in enumerate(table):
        chance=obj["chance"]
        if (randfloat(0,100)<=chance):
            give_item(player,obj["item"],obj["count"])
            if (obj["item"] in given):
                given[obj["item"]]+=obj["count"]
            else:
                given[obj["item"]]=obj["count"]
    return given