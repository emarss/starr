from bible.models import Bible
import json, re

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

def perform_search(key):
    search_results = {}

    bibles = Bible().get_all_bibles()
    bible_names = list(Bible().get_all_bibles().keys())
    key = re.sub('[\s]+', ' ', key);
    key_array = key.split(" ")
    print(key_array)
    for bible in range(0, len(bibles)): #iterating over 66 bibles
        bible_name = bible_names[bible]
        chapters = bibles[bible_name]
        for chapter in range(1, chapters+1): #iterating over chapters, but started at chapter 1
            verses = get_full_chapter(bible_name, chapter);
            verses_contents = list(verses.values());
            for verse in range(1, len(verses)): #iterating over verses starting at 1
                verse_value = verses_contents[verse]

                words_matched = 0;
                for word in range(0, len(key_array)):
                    if re.search(key_array[word], verse_value, re.I):
                        words_matched += 1

                if(words_matched == len(key_array)):
                    verse_key= bible_name + " " + str(chapter) + ":" + str(verse+1);
                    search_results[verse_key] = verse_value;


    return search_results