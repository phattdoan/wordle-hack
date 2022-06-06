import json

## initiate words with 5 letters
words_4 = {}

with open('../data/words_list/words_alpha.txt') as f:
    line = f.readline().strip()
    while line:
        line = f.readline().strip()
        if len(line) >= 4 and len(line) <=7:
            words_4[line] = 1

with open('../data/words_list/spellingbee_words.json', 'w') as f:
    json.dump(words_4, f)