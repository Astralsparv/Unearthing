from ansi import form, col
from util import chance

tiles=[
    { # oob
        "display":" ",
        "name": "OOB",
        "solid":True,
        "id":" "
    },
    { # cave wall
        "display":"#",
        "name": "wall",
        "fgcol": 248,
        "solid":True,
        "id":"#"
    },
    {
        "display":".",
        "name": "floor",
        "fgcol": 8,
        "solid": False,
        "ore_spawnable":5,
        "enemy_spawnable":True,
        "id":"."
    },
    {
        "display":"^",
        "name": "water",
        "fgcol": 32,
        "passthrough_requires_item":"floatie",
        "id":"^"
    },
    {
        "display":"~",
        "name": "water",
        "fgcol": 32,
        "passthrough_requires_item":"floatie",
        "id":"~"
    },
    {
        "display":"f",
        "name": "floatie",
        "fgcol": 196,
        "pickup":"floatie",
        "id":"f"
    },
    {
        "display": ":",
        "name": "ladder",
        "fgcol": 94,
        "id": ":",
        "solid": True
    },
    {
        "display": "o",
        "name": "shaft",
        "fgcol": 94,
        "id": "o",
        "go_to": "new_cave",
        "solid": True
    },
    { # weak soil (mined)
        "display":".",
        "name": "weak_soil_dug",
        "fgcol": 94,
        "solid": False,
        "id":".ws"
    },
    { # weak soil
        "display":",",
        "name": "weak_soil",
        "fgcol": 94,
        "id":",",
        "mineable": {
            "becomes":".ws",
            "loot_table":[
                {
                    "item":"food",
                    "chance":30,
                    "count":1
                },
                {
                    "item":"food",
                    "chance":10,
                    "count":1
                }
            ]
        }
        #form - needed
    },
    { # stone
        "display":"*",
        "name": "stone",
        "id":"S",
        "fgcol": 248,
        "solid": True,
        "ladder_spot": True,
        "ore": -1, # the stone is the default, when no other ores spawn; becomes stone
        "mineable": {
            "becomes":".",
            "loot_table":[
                {
                    "item":"stone",
                    "chance":100,
                    "count":1
                },
                {
                    "item":"stone",
                    "chance":100,
                    "count":1
                }
            ]
        }
    },
    { # coal
        "display":"%",
        "name": "coal",
        "id":"Coal",
        "fgcol": 242,
        "solid": True,
        "ladder_spot": True,
        "ore": 60,
        "mineable": {
            "becomes":".",
            "loot_table":[
                {
                    "item":"coal",
                    "chance":100,
                    "count":1
                },
                {
                    "item":"coal",
                    "chance":10,
                    "count":1
                }
            ]
        }
    },
    { # copper
        "display":"%",
        "name": "copper",
        "id":"Cop",
        "fgcol": 208,
        "solid": True,
        "ladder_spot": True,
        "ore": 55,
        "mineable": {
            "becomes":".",
            "loot_table":[
                {
                    "item":"copper",
                    "chance":100,
                    "count":1
                },
                {
                    "item":"copper",
                    "chance":8,
                    "count":1
                }
            ]
        }
    },
    { # iron
        "display":"%",
        "name": "iron",
        "id":"I",
        "fgcol": 216,
        "solid": True,
        "ladder_spot": True,
        "ore": 40,
        "mineable": {
            "becomes":".",
            "loot_table":[
                {
                    "item":"iron",
                    "chance":100,
                    "count":1
                },
                {
                    "item":"iron",
                    "chance":6,
                    "count":1
                }
            ]
        }
    },
    { # gold
        "display":"%",
        "name": "gold",
        "id":"G",
        "fgcol": 220,
        "solid": True,
        "ladder_spot": True,
        "ore": 30,
        "mineable": {
            "becomes":".",
            "loot_table":[
                {
                    "item":"gold",
                    "chance":100,
                    "count":1
                },
                {
                    "item":"gold",
                    "chance":3,
                    "count":1
                }
            ]
        }
    }
]

char_to_tile={
    tile["id"]: i
    for i, tile in enumerate(tiles)
}

ores=[]
for _, tile in enumerate(tiles):
    if ("ore" in tile):
        ores.append({
            "chance":tile["ore"],
            "ore":tile["id"]
        })

def tile_render(tile,fgcol=True,bgcol=True):
    if (not isinstance(tile, int)):
        return str(tile)
    if (tile>=0 and len(tiles)>tile):
        obj=tiles[tile]
        fg=obj.get("fgcol")
        bg=obj.get("bgcol")
        if ("form" in obj):
            return form(obj["display"],obj["form"])
        if "fgcol" in obj or "bgcol" in obj:
            return col(
                obj["display"],
                fgcol=obj.get("fgcol"),
                bgcol=obj.get("bgcol"),
            )
        return obj["display"]
    else:
        return str(tile)

def is_solid(tile):
    if (tile>=0 and len(tiles)>tile):
        if ("solid" in tiles[tile]):
            return tiles[tile]["solid"]==True
    return False

def passthrough_item_required(tile):
    if (tile>=0 and len(tiles)>tile):
        if ("passthrough_requires_item" in tiles[tile]):
            return tiles[tile]["passthrough_requires_item"]
    return None

def is_interactable(tile):
    if (tile>=0 and len(tiles)>tile):
        if ("pickup" in tiles[tile]):
            return "pickup",tiles[tile]["pickup"]
        if ("go_to" in tiles[tile]):
            return "go_to",tiles[tile]["go_to"]
    return False,None

def is_mineable(tile):
    if (tile>=0 and len(tiles)>tile):
        if ("mineable" in tiles[tile]):
            return tiles[tile]["mineable"]
    return False

def can_spawn_ores(tile):
    if (tile>=0 and len(tiles)>tile):
        if ("ore_spawnable" in tiles[tile]):
            return tiles[tile]["ore_spawnable"]
        return 0
    else:
        return 0

# should be affected by player luck & player depth
def get_ore_to_spawn():
    # base 50% chance whether it should even try spawning a mineral, or should just pick stone
    if (chance(50)):
        for _,ore in enumerate(ores):
            if (chance(ore["chance"])):
                return ore["ore"]
    return "S" # stone, might make to return whatever is -1 later, unsure

def tile_name(tile):
    return tiles[tile]["name"]