"""
    Objective: solve New York Times Spelling Bee game
    Author: Phat Doan
    Date: 5/29/2022
    
"""


import json
import utils

def main():
    with open('../data/words_list/spellingbee_words.json') as json_file:
        words = json.load(json_file)

    results = []

    center_letter = input("Enter center letter: ")
    letter_hive = input("Enter 6 surround character: ")
    letter_list = utils.convert_string_to_list(letter_hive)
    hive_list = [center_letter] + letter_list
    
    for word in words:
        word_flag = True
        for letter in word:
            if letter not in (hive_list):
                word_flag = False
                break

        if word_flag == True:
            if center_letter in utils.convert_string_to_list(word):
                results += [word]

    print(results)

if __name__ == "__main__":
    main()