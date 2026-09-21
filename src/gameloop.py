import modes.caving.main as caving
import modes.title as title
import modes.pause as pause
import modes.save as save
import manager

def update():
    if (manager.current_section=="title"):
        title.update()
    elif (manager.current_section=="caving"):
        caving.update()
    elif (manager.current_section=="pause"):
        pause.update()
    elif (manager.current_section=="save"):
        save.update()

def draw():
    if (manager.current_section=="title"):
        title.draw()
    elif (manager.current_section=="caving"):
        caving.draw()
    elif (manager.current_section=="pause"):
        pause.draw()
    elif (manager.current_section=="save"):
        save.draw()