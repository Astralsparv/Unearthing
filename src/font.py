# custom font renderer (assets/font/title.json for example)
# fonts may not have all characters, if so; it renders as a space.
# more like converts to a str rather than rendering though

# fonts are json files, where "a":str and str is mult-line
# font["sep"] == the seperator between the characters (num)

import json
def load_font(font):
    with open(f"assets/fonts/{font}.json") as f:
        return json.load(f)

def render_char(font,char):
    return font.get(char,font[" "])

def render_str(font,string):
    if (string==""):
        return ""
    # woah new trick
    sepstr=" "*font.get("sep", 1)

    # get font height
    height=max(
        len(glyph.splitlines())
        for key, glyph in font.items()
        if key != "sep"
    )

    chars=[]
    for char in string:
        lines=render_char(font, char).splitlines()

        width=max(
            (len(line) for line in lines),
            default=0
        )

        # pad each line
        lines=[
            line.ljust(width)
            for line in lines
        ]

        # pad rows to be same height as tallest char
        lines.extend(
            [" "*width]*(height-len(lines))
        )

        chars.append(lines)

    if (not chars):
        return ""

    lines=[]

    return "\n".join(
        sepstr.join(char[y] for char in chars)
        for y in range(height)
    )