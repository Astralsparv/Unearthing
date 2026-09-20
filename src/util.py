from random import random

def chance(perc):
    return (random()*100<=perc)

def wrap(text, width):
    text=str(text)

    if (width<=0):
        return ""
    lines=[]

    for line in text.split("\n"):
        words=line.split(" ")
        current=""
        for word in words:
            # length of word > width
            # even if put on new line, wouldnt fit
            while (len(word)>width):
                if (current):
                    lines.append(current)
                    current=""

                lines.append(word[:width])
                word=word[width:]

            if (not word):
                continue

            if (not current):
                current=word
            elif (len(current)+1+len(word)<=width):
                current+=" "+word
            else:
                lines.append(current)
                current=word

        if (current):
            lines.append(current)

    return "\n".join(lines)

direction_as_word={
    "w": "up",
    "a": "left",
    "s": "down",
    "d": "right"
}