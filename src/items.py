from util import chance

def give_item(player,item,count):
    for i in range(len(player["inventory"])):
        if (player["inventory"][i]["item"]==item):
            player["inventory"][i]["count"]+=count
            return
    player["inventory"].append({
        "item":item,
        "count":count
    })

def give_loot_table(player,table):
    given={}
    for i,obj in enumerate(table):
        perc=obj["chance"]
        if (chance(perc)):
            give_item(player,obj["item"],obj["count"])
            if (obj["item"] in given):
                given[obj["item"]]+=obj["count"]
            else:
                given[obj["item"]]=obj["count"]
    return given

items={
    "pickaxe":{
        "type": "tool",
        "damage_tiles": 1,
        "range_infront":[0,1,0],
        "animation": "tile_infront" # break infront
    },
    "sword":{
        "type": "weapon",
        "damage_enemies": 1,
        "range_infront":[1,1,1],
        "animation": "swipe_infront" # swiping anim
    },
    "stone":{
        "type": "resource"
    },
    "coal":{
        "type": "resource"
    },
    "copper":{
        "type": "resource"
    },
    "iron":{
        "type": "resource"
    },
    "gold":{
        "type": "resource"
    },
    "food":{
        "type": "food",
        "energy": 5,
        "health": 5,
        "lose":1
    }
}

def item_properties(obj):
    if (type(obj)=="string"):
        item=items[obj]
    else:
        item=items[obj["item"]]
    return item

def can_use(obj):
    item=item_properties(obj)
    return ("energy" in item or "health" in item or "damage_enemies" in item or "damage_tiles" in item)