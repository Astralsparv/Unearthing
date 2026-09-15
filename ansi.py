def form(txt,form):
    return form+txt+"\x1b[0m"


def col(string, fgcol=255, bgcol=233):
    if (fgcol==None):
        fgcol=255
    if (bgcol==None):
        bgcol=233
    
    return (
        f"\x1b[38;5;{fgcol}m"
        f"\x1b[48;5;{bgcol}m"
        f"{string}"
        f"\x1b[0m"
    )

if (False): # debug; view color table
    colors=[
        f"\x1b[48;5;{i}m"
        for i in range(256)
    ]
    input("\n".join(
        "".join(
            f"{colors[i]}{i:3d}\x1b[0m "
            for i in range(row,row+16)
        )
        for row in range(0, 256, 16)
    )+"\n")