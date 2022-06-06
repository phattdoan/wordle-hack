import json

words_5 = {}

with open('../data/words_list/wordle_word_source.txt') as f:
    line = f.readline().strip()
    while line:
        line = f.readline().strip()
        words_5[line] = 1

with open('../data/words_list/wordle_words_source.json', 'w') as f:
    json.dump(words_5, f)