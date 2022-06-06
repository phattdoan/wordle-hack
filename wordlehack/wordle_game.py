"""
Wordle game
Author: Phat Doan
Date: 5/13/2022
"""

import json
import random
import utils

class WordleGame:

    def __init__(self):
        self.alphabet = {'a':0
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

    def get_a_word(self):
        """
            objective: get a word of 5 letter from the words list
            return: a 5 letter word
        """
        with open('../data/words_list/wordle_words_source.json') as json_file:
            words = json.load(json_file)

        # generate a random word
        num_rand = random.randint(0, len(words))
        for i,word in enumerate(words):
            if i == num_rand:
                break

        return(word)

    def check_word_input(self, user_input):
        """
            Objective: check user input for wordle
                must be 5 alphabet letter
            return: True for pass and False for failure
        """

        flag = True
        if len(user_input) != 5:
            flag = False

        for alp in user_input:
            if alp not in self.alphabet:
                flag = False
                break

        return(flag)

    def get_input(self, guess_count):
        """
            Objective: get a guess word from the user
            return: validated string
        """
        # COUNT_DICT = {1:"first"
        #                 ,2:"second"
        #                 ,3:"third"
        #                 ,4:"fourth"
        #                 ,5:"fifth"}
        flag = False
        while flag == False:           
            guess_word = input("Please enter your guess: ")
            
            if self.check_word_input(guess_word):
                flag = True
            else:
                print("Please enter a 5 letter word")

        return guess_word


    def compare_guess_to_word(self, guess, word):
        """
            Objective: check guess word against the Wordle word
            return: a string that represent the match
                _ for not match
                y for letter that is in the word but not the right position
                g for match
        """
        
        match_result = ""

        list_string = utils.convert_string_to_list(word)

        for i, alp in enumerate(word):
            if guess[i] == word[i]:
                match_result += "g"
            else:
                if guess[i] in list_string:
                    match_result += 'y'
                else:
                    match_result += "_"

        return match_result

    def check_win(self, match_result):
        """
            Objective: check for win ggggg
            return: Boolean
                True for win
                False for not
        """
        if match_result == 'ggggg':
            return(True)
        else:
            return(False)

def main():
    """
        Objective: run wordle
    """
    game = WordleGame()
    word = game.get_a_word()

    print("Let's play Worlde!")

    match_record = {}

    for i in range(1,6):
        print("----------------------------------------------------")
        print("Guess " + str(i) + " :")
        guess_word = game.get_input(i)
        print(guess_word)
        
        match_result = game.compare_guess_to_word(guess_word, word)
        print(match_result)

        match_record[i] = [guess_word, match_result]
        if game.check_win(match_result):
            print("You guessed it!")
            break

    print("Game end!")
    print(word)
    print(match_record)


if __name__ == "__main__":
    main()