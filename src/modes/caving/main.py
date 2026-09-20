from graphics import draw_at,cprint,clear,render,curs,curs_offset,draw_at_col
from tiles import tile_render,is_interactable,tiles,tile_name
import manager
from manager import mset, mget, set_map_programatically, text
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from items import give_loot_table, give_item, can_use, item_properties
from manager import get_key, current_item
from util import chance,wrap

from modes.caving.player import update_player_actions
from modes.caving.draw import draw as _draw
from modes.caving.entities import draw_entities, update_entities, spawn_entities
from modes.caving.helper import do_needed_animations,rendering_game

spawn_entities()

def draw():
    clear()
    _draw()
    draw_entities()
    rendering_game(True)
    do_needed_animations()
    rendering_game(False)
    render()

def update():
    if (update_player_actions()):
        update_entities()