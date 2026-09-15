from random import randrange as randfloat

def give_item(player,item,count):
    if (item in player["inventory"]):
        player["inventory"][item]+=count
    else:
        player["inventory"][item]=count

def give_loot_table(player,table):
    for i,obj in enumerate(table):
        chance=obj["chance"]
        if (randfloat(0,100)<=chance):
            give_item(player,obj["item"],obj["count"])