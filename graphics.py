def clear():
    print("\033[H\033[2J", end="")

def draw_at(x,y,c):
    print("\033[{0};{1}H{2}".format(y, x, c))