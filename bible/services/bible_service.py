import json

def format_chapter(bk, ch): 
    return str(bk) + " " + str(ch)

def format_verse(bk, ch, vs):
    return format_chapter(bk, ch) + ":" + str(vs)

def get_verse(book, fvs):
    return book[fvs]

def get_full_chapter(bk, ch):
    bk_name = "media/bible/esv/" + bk + ".json"
    file = open(bk_name)
    book = json.load(file)
    keys = book.keys()

    new_ch = {}
    vs = 1
    while True:
        fvs = format_verse(bk, ch, vs)
        if fvs in keys:
            new_ch[fvs] = get_verse(book, fvs)
        else:
            break
        vs = vs + 1
    return new_ch
