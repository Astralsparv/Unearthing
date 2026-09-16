from ansi import form, col

tiles=[
    { # oob
        "display":" ",
        "solid":True,
        "id":" "
    },
    { # cave wall
        "display":"#",
        "fgcol": 248,
        "solid":True,
        "id":"#"
    },
    {
        "display":".",
        "fgcol": 8,
        "solid": False,
        "ore_spawnable":5,
        "enemy_spawnable":True,
        "id":"."
    },
    {
        "display":"^",
        "fgcol": 32,
        "passthrough_requires_item":"floatie",
        "id":"^"
    },
    {
        "display":"~",
        "fgcol": 32,
        "passthrough_requires_item":"floatie",
        "id":"~"
    },
    {
        "display":"f",
        "fgcol": 196,
        "pickup":"floatie",
        "id":"f"
    },
    {
        "display": ":",
        "fgcol": 94,
        "id": ":"
    },
    {
        "display": "o",
        "fgcol": 94,
        "id": "o",
        "go_to": "new_cave"
    },
    { # weak soil (mined)
        "display":".",
        "fgcol": 94,
        "solid": False,
        "id":".ws"
    },
    { # weak soil
        "display":",",
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
        "id":"S",
        "fgcol": 248,
        "solid": True,
        "ladder_spot": True,
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
                    "chance":30,
                    "count":1
                }
            ]
        }
        #form - needed
    },
    { # coal
        "display":"%",
        "id":"C",
        "solid": True,
        "ladder_spot": True
        #form - needed
    },
    { # iron
        "display":"%",
        "id":"I",
        "solid": True,
        "ladder_spot": True
        #form - needed
    },
    { # gold
        "display":"%",
        "id":"G",
        "solid": True,
        "ladder_spot": True
        #form - needed
    }
]

char_to_tile={
    tile["id"]: i
    for i, tile in enumerate(tiles)
}

def tile_render(tile):
    if (not isinstance(tile, int)):
        return str(tile)
    if (tile>=0 and len(tiles)>tile):
        obj=tiles[tile]
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