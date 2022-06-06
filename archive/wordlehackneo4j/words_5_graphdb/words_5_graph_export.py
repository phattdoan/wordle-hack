"""


"""
import json


def Convert_string_to_list(string):
    """
    
    """
    list_string = []
    list_string[:0] = string
    
    return list_string


with open('../words_list/wordle_words.json') as json_file:
    words = json.load(json_file)


"""with open('../words_list/words_5_graph.csv','w') as file:
    file.write('word,letter1,letter2,letter3,letter4,letter5\n')

    for i,word in enumerate(words):
        alph_list = Convert_string_to_list(word)
        file.write(word)
        for alph in alph_list:
            file.write(',' + alph)
        file.write('\n')
"""

with open('../words_5_graphdb/words_5_graph.csv','w') as file:
    file.write('word,alphabet,position\n')

    for i,word in enumerate(words):
        alph_list = Convert_string_to_list(word)
        
        for i, alph in enumerate(alph_list):
            file.write(word)
            file.write(',' + alph + ',' + str(i+1))
            file.write('\n')



with open('../words_5_graphdb/words_5.csv','w') as file:
    file.write('word\n')

    for i,word in enumerate(words):
        file.write(word)
        file.write('\n')

with open('../words_5_graphdb/alphabet.csv','w') as file:
    file.write('alphabet\n')
    file.write('a\n')
    file.write('b\n')
    file.write('c\n')
    file.write('d\n')
    file.write('e\n')
    file.write('f\n')
    file.write('g\n')
    file.write('h\n')
    file.write('i\n')
    file.write('j\n')
    file.write('k\n')
    file.write('l\n')
    file.write('m\n')
    file.write('n\n')
    file.write('o\n')
    file.write('p\n')
    file.write('q\n')
    file.write('r\n')
    file.write('s\n')
    file.write('t\n')
    file.write('u\n')
    file.write('v\n')
    file.write('w\n')
    file.write('x\n')
    file.write('y\n')
    file.write('z')