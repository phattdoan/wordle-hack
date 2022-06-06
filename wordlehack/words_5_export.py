import json

## alphabet count
alphabet = {'a':0
            ,'b':0
            ,'c':0
            ,'d':0
            ,'e':0
            ,'f':0
            ,'g':0
            ,'h':0
            ,'i':0
            ,'j':0
            ,'k':0
            ,'l':0
            ,'m':0
            ,'n':0
            ,'o':0
            ,'p':0
            ,'b':0
            ,'q':0
            ,'r':0
            ,'s':0
            ,'t':0
            ,'u':0
            ,'v':0
            ,'w':0
            ,'x':0
            ,'y':0
            ,'z':0}

## initiate words with 5 letters
words_5 = {}

with open('../words_list/words_alpha.txt') as f:
    line = f.readline().strip()
    while line:
        line = f.readline().strip()
        if len(line) == 5:
            words_5[line] = 1
            for alp in line:
                alphabet[alp] += 1

print(len(words_5))

print(alphabet)

with open('../words_list/wordle_words.json', 'w') as f:
    json.dump(words_5, f)