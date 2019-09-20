from lxml import etree
import csv
import json



def get_words():
    with open('_data/word_list.json', encoding="utf_8") as fd:
        json_data = json.load(fd)
        return json_data
    

def get_radical_meanings():
    response = []
    with open('_data/radical_meanings.csv', encoding='utf_8') as csv_file:
        reader = csv.reader(csv_file)
        first_line = True
        for row in reader:
            if first_line == True:
                first_line = False
                continue
            response.append({
                'radical' : row[0][0],
                'stroke_count' : row[1],
                'meaning' : row[3]
            })
    return response
            

def radical_generator():
    file = open('_data/kradfile.utf', 'r', encoding='utf_8')
    for line in file:
        kanji, rad_string = line.split(' : ')
        # print(kanji)
        radicals = rad_string.replace('\n', '').split(' ')
        yield {
            'kanji' : kanji,
            'radicals' : radicals,
        }


def intialize_entry():
    return {
        'on_yomis' : [],
        'kun_yomis' : [],
        'meanings' : []
    }


def kanjidic_generator():
    entry = intialize_entry()
    KANJIDIC = '_data/kanjidic2.utf'
    for event, elem in etree.iterparse(KANJIDIC, events=('end', )):
        if event == 'end':
            # if closing a character section, return entry dict and start over
            if elem.tag == 'character':
                yield(entry)
                entry = intialize_entry()
            
            # append various elements to entry dict
            if elem.tag == 'literal':
                entry['kanji'] = elem.text
            if elem.tag == 'grade':
                entry['grade'] = elem.text
            if elem.tag == 'stroke_count':
                entry['stroke_count'] = elem.text
            if elem.tag == 'freq':
                entry['popularity'] = elem.text
            if elem.tag == 'jlpt':
                entry['jlpt_level'] = elem.text
            if elem.tag == 'meaning' and not 'm_lang' in elem.attrib:
                entry['meanings'].append(elem.text)
            if elem.tag == 'reading' and elem.attrib['r_type'] == 'ja_on':
                on_yomis = elem.text.split('.')
                entry['on_yomis'] += on_yomis
            if elem.tag == 'reading' and elem.attrib['r_type'] == 'ja_kun':
                kun_yomis = elem.text.split('.')
                entry['kun_yomis'] += kun_yomis
            
            # we're done with this element so lets free up that space
            elem.clear()
            
            
            
            
            
            
            
            
            
            
