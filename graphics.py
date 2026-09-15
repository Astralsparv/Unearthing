def clear():
    print("\033[H\033[2J", end="")

# 0,0 == 1,1
def draw_at(x,y,c):
    x+=1
    y+=1
    print("\033[{0};{1}H{2}".format(y, x, c))