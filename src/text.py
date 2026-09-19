import json

def getLang(lang):
    dat={}
    with open(f"assets/langs/{lang}.json","r") as f:
        dat=json.load(f)
    return dat

def getText(lang,fullid,opts=[]):
    sects=fullid.split('.') #actions.swing_pickaxe.hit_nothing
    text=lang
    for _,sect in enumerate(sects):
        if (not sect in text):
            return fullid
        text=text[sect]

    for i, value in enumerate(opts, start=1): # add opts
        text=text.replace(f"%{i}", str(value))
    return text