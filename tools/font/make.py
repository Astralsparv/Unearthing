import json
import os

font={}

font_loc=input("Location of font source folder:")
case_sensitive=""
bools={
    "y":True,
    "n":False,
    "yes":True,
    "no":False,
    "true":True,
    "false":False
}
while (not case_sensitive.lower() in bools):
    case_sensitive=input("Is case sensitive?\n")
case_sensitive=bools[case_sensitive.lower()]
print(case_sensitive)
for i in range(95): # all ascii
    # skip 32; space
    char=chr(i+33) # to string
    path=f"{font_loc}/{char}.txt"
    if (os.path.isfile(path)):
        with open(path,"r") as r:
            font[char]=r.read()

        spl=font[char].split("\n")

        longest=0
        for line in spl:
            n=len(spl)
            if (n>longest):
                longest=n

        txt=""
        for line in spl:
            l=line
            while (len(l)<longest):
                l+=" "
            txt+=l+"\n"

        font[char]=txt

        if (case_sensitive==False):
            if (char.isupper()):
                font[char.lower()]=font[char]
            else:
                font[char.upper()]=font[char]

def getNum(txt):
    print(txt)
    v=input("")
    while (not v.isnumeric()):
        v=input("")
    return int(v)

space=getNum("What is the length of the space?")
txt=""
for i in range(space):
    txt+=" "
font[" "]=txt

seperator=getNum("What is the length between characters?")
font["sep"]=seperator

with open("font.json","w") as f:
    json.dump(font,f)