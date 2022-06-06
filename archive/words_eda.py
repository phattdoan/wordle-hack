import json

with open('words_list/wordle_words.json') as json_file:
    words = json.load(json_file)

def Convert_string_to_list(string):
    """
    
    """
    list_string = []
    list_string[:0] = string
    
    return list_string

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


for letter_position in range(0,5):
    alphabet_position = alphabet
    for word in words:
         alphabet[Convert_string_to_list(word)[letter_position]] += 1
    
    print(alphabet_position)
