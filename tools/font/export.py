import json
import os

font_loc=input("Location of font file:")

font={}
with open(font_loc,"r") as f:
    font=json.load(f)

exp=input("Location of export:")
os.makedirs(exp,exist_ok=True)

for key,val in font.items():
    with open(f"{exp}/{key}.txt","w") as f:
        f.write(val)

print("DONE!")