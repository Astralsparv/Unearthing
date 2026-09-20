from graphics import draw_at_col,render,get_char, draw_at_prec, draw_at
from tiles import tile_render
import time
from manager import mget
import manager
import math

WIDTH,HEIGHT=80,24
def circle_frame(radius,char=" ",fgcol=255,bgcol=232):
    def draw(dx,dy): #dx,dy not needed
        points=[]

        for oy in range(-HEIGHT, HEIGHT + 1):
            for ox in range(-WIDTH, WIDTH + 1):

                # *2 since the height of a char is roughly double width
                # makes it look more like a perfect circle

                # x^2+y^2=r^2
                # ox^2+(oy*2)^2

                # if ox^2+(oy*2)^2 > r^2 then its not in the circle
                if (((ox*ox)+(oy*2)*(oy*2))>(radius*radius)):
                    points.append((ox,oy,char,fgcol,bgcol))

        return points

    return draw

def swipe_curve(dx,dy):
    if (dx==0):
        return "-"
    else:
        if (dx==1):
            return ")"
        else:
            return "("

def swipe_point(dy):
    if (dy==1):
        return "'"
    else:
        return "."

animations={
    "damage_player":{
        "player_visible": True,
        "frames":[
            {
                "draw": lambda dx,dy:[
                    (0,0,"X",196,None)
                ],
                "duration": 0.1
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,"@",196,None)
                ],
                "duration": 0.3
            }
        ]
    },
    "hit_tile":{
        "player_visible": True,
        "frames":[
            {
                "draw": lambda dx,dy:[
                    (0,0,"X",255,None)
                ],
                "duration": 0.1
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,"*",255,None)
                ],
                "duration": 0.1
            }
        ]
    },
    "sword_swipe":"directional",
    "sword_swipe_vert":{
        "player_visible": True,
        "frames":[
            {
                "draw": lambda dx,dy:[
                    (0,-1,"'",255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (0,-1,"'",249,None),
                    (0,0,swipe_curve(dx,dy),255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,swipe_curve(dx,dy),255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,swipe_curve(dx,dy),249,None),
                    (0,1,".",255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (0,1,".",255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (0,1,".",249,None)
                ],
                "duration": 0.05
            }
        ]
    },
    "sword_swipe_hoz":{
        "player_visible": True,
        "frames":[
            {
                "draw": lambda dx,dy:[
                    (-1,0,swipe_point(dy),255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (-1,0,swipe_point(dy),249,None),
                    (0,0,swipe_curve(dx,dy),255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,swipe_curve(dx,dy),255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,swipe_curve(dx,dy),249,None),
                    (1,0,swipe_point(dy),255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (1,0,swipe_point(dy),255,None)
                ],
                "duration": 0.05
            },
            {
                "draw": lambda dx,dy:[
                    (1,0,swipe_point(dy),249,None)
                ],
                "duration": 0.05
            }
        ]
    },
    "descend_into_shaft":{
        "player_visible": False,
        "frames":[
        {
            "draw": lambda dx,dy:[
                    (0,0,"@",255,None)
                ],
                "duration": 0.1
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,"@",250,None)
                ],
                "duration": 0.1
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,"@",245,None)
                ],
                "duration": 0.1
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,"@",240,None)
                ],
                "duration": 0.1
            },
            {
                "draw": lambda dx,dy:[
                    (0,0,"@",235,None)
                ],
                "duration": 0.1
            }
        ]
    },
    "circle_in":{
        "player_visible": True,
        "frames":[
            {
		"draw": circle_frame(25),
		"duration": 0.001
	},{
		"draw": circle_frame(24),
		"duration": 0.001
	},{
		"draw": circle_frame(23),
		"duration": 0.001
	},{
		"draw": circle_frame(22),
		"duration": 0.001
	},{
		"draw": circle_frame(21),
		"duration": 0.001
	},{
		"draw": circle_frame(20),
		"duration": 0.001
	},{
		"draw": circle_frame(19),
		"duration": 0.001
	},{
		"draw": circle_frame(18),
		"duration": 0.001
	},{
		"draw": circle_frame(17),
		"duration": 0.001
	},{
		"draw": circle_frame(16),
		"duration": 0.001
	},{
		"draw": circle_frame(15),
		"duration": 0.001
	},{
		"draw": circle_frame(14),
		"duration": 0.001
	},{
		"draw": circle_frame(13),
		"duration": 0.001
	},{
		"draw": circle_frame(12),
		"duration": 0.001
	},{
		"draw": circle_frame(11),
		"duration": 0.001
	},{
		"draw": circle_frame(10),
		"duration": 0.001
	},{
		"draw": circle_frame(9),
		"duration": 0.001
	},{
		"draw": circle_frame(8),
		"duration": 0.001
	},{
		"draw": circle_frame(7),
		"duration": 0.001
	},{
		"draw": circle_frame(6),
		"duration": 0.001
	},{
		"draw": circle_frame(5),
		"duration": 0.001
	},{
		"draw": circle_frame(4),
		"duration": 0.001
	},{
		"draw": circle_frame(3),
		"duration": 0.001
	},{
		"draw": circle_frame(2),
		"duration": 0.001
	},{
		"draw": circle_frame(1),
		"duration": 0.001
	},
        ]
    },
    "circle_out":{
        "player_visible": True,
        "frames":[
            {
                "draw": circle_frame(1),
                "duration": 0.001
            },{
                "draw": circle_frame(2),
                "duration": 0.001
            },{
                "draw": circle_frame(3),
                "duration": 0.001
            },{
                "draw": circle_frame(4),
                "duration": 0.001
            },{
                "draw": circle_frame(5),
                "duration": 0.001
            },{
                "draw": circle_frame(6),
                "duration": 0.001
            },{
                "draw": circle_frame(7),
                "duration": 0.001
            },{
                "draw": circle_frame(8),
                "duration": 0.001
            },{
                "draw": circle_frame(9),
                "duration": 0.001
            },{
                "draw": circle_frame(10),
                "duration": 0.001
            },{
                "draw": circle_frame(11),
                "duration": 0.001
            },{
                "draw": circle_frame(12),
                "duration": 0.001
            },{
                "draw": circle_frame(13),
                "duration": 0.001
            },{
                "draw": circle_frame(14),
                "duration": 0.001
            },{
                "draw": circle_frame(15),
                "duration": 0.001
            },{
                "draw": circle_frame(16),
                "duration": 0.001
            },{
                "draw": circle_frame(17),
                "duration": 0.001
            },{
                "draw": circle_frame(18),
                "duration": 0.001
            },{
                "draw": circle_frame(19),
                "duration": 0.001
            },{
                "draw": circle_frame(20),
                "duration": 0.001
            },{
                "draw": circle_frame(21),
                "duration": 0.001
            },{
                "draw": circle_frame(22),
                "duration": 0.001
            },{
                "draw": circle_frame(23),
                "duration": 0.001
            },{
                "draw": circle_frame(24),
                "duration": 0.001
            },{
                "draw": circle_frame(25),
                "duration": 0.001
            }
        ]
    }
}

def animate(name,x,y,dx=0,dy=0,offsetX=0,offsetY=0):
    x=int(x)
    y=int(y)
    offsetX=int(offsetX)
    offsetY=int(offsetY)
    if (animations[name]=="directional"):
        if (dx==0):
            name+="_hoz"
        else:
            name+="_vert"

    if (animations[name]["player_visible"]==False):
        t=mget(manager.player["x"],manager.player["y"])
        draw_at(manager.player["x"],manager.player["y"],tile_render(t))
    for frame in animations[name]["frames"]:
        original={}
        for ox, oy, char, fgcol, bgcol in frame["draw"](dx,dy):
            px=x+ox
            py=y+oy
            if ((px,py) not in original):
                original[(px,py)]=get_char(px,py)
            
            draw_at_col(
                px,
                py,
                char,
                fgcol=fgcol,
                bgcol=bgcol
            )

        render()
        time.sleep(frame["duration"])

        for (px, py), cell in original.items():
            draw_at_prec(px,py,cell[0],cell[1])