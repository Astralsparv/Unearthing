formatting={
    "f":"\x1b[1;31m", # red floaty
    "~":"\x1b[1;94m", # water
    "^":"\x1b[1;94m", # water
    ".":"\x1b[1;90m"  # floor
}

def form(txt,form):
    return form+txt+"\x1b[0m"

def pretty(chr):
    if (chr in formatting):
        return form(chr,formatting[chr])
    return chr