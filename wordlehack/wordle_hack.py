"""
Wordle game hack
Author: Phat Doan
Date: 5/13/2022
Last update: 5/29/2022
Version: MVP

Proposed steps:
    . Initiate the wordle game
    . Start with a pre-determined seed word
    . Analyze the result from seed word
        . Prune word list to possible remaining words against results
            . Black and green positions are used to groom possible words
        . Compute a feedforward neural matrix of 26(alphabet)x5(positions): += 1/total remaing words count
            . Yellow positions are used in conjunction with other to create probabilities for possible words
            . Assign a probability to the remaining words: sum(P(alphabet|position))
            . Guess the next word based on the highest probability
    . Repeat process until finding the correct word

To do:
    . Strategy to avoidn gggg_ where the last letter could lead to multiple similar guesses. Example:
        decal, decaf, decan, decay
    . Map letter to a 1 to 1

"""

from wordle_game import WordleGame
import utils
import json

class WordleHack:
    """
        Objective:
            . Get a guess word and the wordle result
            . Generate a search query
            . Retrieve possible results and its probability
            . Create a new guess word based on uniqueness until guess 5 then pick highest probability
    """

    def __init__(self, seed_word = "adieu"):
        """
            arg: seed_word: start word
            uraei
            arise
            kades
        """
        self.SEED_WORD = seed_word
       
        with open('../data/words_list/wordle_words_source.json') as json_file:
             self.WORDLE_WORDS_DICT = json.load(json_file)

        self.possible_words_dict = self.WORDLE_WORDS_DICT

        """
            result_dict:
            0: not matched alphabet
            1-5: position of the alphabet
                y: yellow (not matched position)
                g: green (matched position)
            store results of all guesses
        """

        self.result_dict = {1:{'y':[]
                         ,'g':""}
                      ,2:{'y':[]
                         ,'g':""}
                      ,3:{'y':[]
                         ,'g':""}
                      ,4:{'y':[]
                         ,'g':""}
                      ,5:{'y':[]
                         ,'g':""}
                      ,0:[]
                      ,'gy':[]}

        """
            match_record: {1:[___gy]
                          ,2:[____g]}
        """
        self.match_record = {}

    def get_result(self):
        return(self.result_dict)

    # def get_markov_matrix(self):
    #     return(self.markov_matrix)

    def get_seed_word(self):
        """
            Objective: return initial seed word
        """
        return(self.SEED_WORD)

    def get_possible_word_dict(self):
        return(self.possible_words_dict)

    def get_match_record(self):
        return(self.match_record)

    def check_result(self, guess, result):
        """
            Objective: check the latest guess and its result and store it in self.result
            args:
                guess: the guess word (i.e. hello)
                result: result from wordle guess word (i.e. __yg_y)
        """
        for i,r in enumerate(result):
            if r == 'g':
                if guess[i] != self.result_dict[i+1]['g']:
                    self.result_dict[i+1]['g'] = guess[i]
                if guess[i] not in self.result_dict['gy']:
                    self.result_dict['gy'] += guess[i]
            elif r == 'y':
                if guess[i] not in self.result_dict[i+1]['y']:
                    self.result_dict[i+1]['y'].append(guess[i])
                if guess[i] not in self.result_dict['gy']:
                    self.result_dict['gy'] += guess[i]
            else:
                if guess[i] not in self.result_dict[0]:
                    self.result_dict[0].append(guess[i])

    def prune_word_list(self):
        """
            Objective: to prune the current word dict to possible answers
            Args:
                Self to get self.WORDLE_WORDS_DICT
            Return:
                self.possible_words_dict
        """
        for word in self.possible_words_dict.copy():
            word_string_list = utils.convert_string_to_list(word)

            ## possible words must contain all green and yellow letters
            if len(list(set(self.result_dict['gy']).intersection(set(word_string_list)))) != len(self.result_dict['gy']):
                del self.possible_words_dict[word]
            else:
                for i, letter in enumerate(word_string_list):
                    ## check if the letter is a match to green
                    if self.result_dict[i+1]['g']:
                        if  letter != self.result_dict[i+1]['g']:
                            del self.possible_words_dict[word]
                            break

                    ## check if the letter violate other rule (alphabet that were excluded or not in the right position)
                    if letter in self.result_dict[0] or letter in self.result_dict[i+1]['y']:
                        del self.possible_words_dict[word]
                        break

                    ## check if other letters match current y position
                    if self.result_dict[i+1]['y']:
                        word_list_minus_i = word_string_list.copy()
                        word_list_minus_i.pop(i)

                        y_letter_match_count = 0
                        for y_letter in self.result_dict[i+1]['y']:
                            if y_letter in word_list_minus_i:
                                y_letter_match_count += 1
                                break
                                
                        if y_letter_match_count == 0:
                            del self.possible_words_dict[word]
                            break
                
            

    def generate_guess(self):
        """
            Given a list of possible words from previous guesses, generate the next guess based on most frequently appears alphabet, accounting for result dictionary
            arg:
                word_list: list of possible words based on previous guesses
            return: a word based on highest probability

        """
        alphabet_position_probability_dict = {'a':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'b':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'c':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'d':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'e':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'f':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'g':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'h':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'i':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'j':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'k':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'l':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'m':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'n':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'o':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'p':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'q':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'r':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'s':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'t':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'u':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'v':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'w':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'x':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'y':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                            ,'z':{1:0
                                                ,2:0
                                                ,3:0
                                                ,4:0
                                                ,5:0}
                                                }

        if len(self.possible_words_dict) == 1:
            return(list(self.possible_words_dict.keys())[0])
        else:
            ## to make a guess based on highest probability of a word
            for i in range(1,6):
                if self.result_dict[i]['g'] != '':
                    alphabet_position_probability_dict[self.result_dict[i]['g']][i] = 1
                else:
                    for word in self.possible_words_dict:
                        alphabet_position_probability_dict[word[i-1]][i] += 1

            ## calculate probability of a letter occurs in the remaining possible list
            for i in range(1,6):
                if self.result_dict[i]['g'] != '':
                    pass
                else:        
                    for letter in alphabet_position_probability_dict:
                        alphabet_position_probability_dict[letter][i] = alphabet_position_probability_dict[letter][i]/len(self.possible_words_dict)            

            ## assign probability to each remaining word, based on their letter probability
            for word in self.possible_words_dict:
                word_prob = 0
                for i, letter in enumerate(word):
                    word_prob += alphabet_position_probability_dict[letter][i+1]
                self.possible_words_dict[word] = word_prob
            
            guess_word = max(self.possible_words_dict, key= self.possible_words_dict.get)
            return(guess_word)


def main():
    """
        Objective: run wordle
    """
    print("Let's play Worlde!")
    game = WordleGame()
    wordle_word = game.get_a_word()
    # wordle_word = 'creak'
    print("Wordle word is:", wordle_word)

    match_record = {}
    hack = WordleHack()

    """ 
        Initiate guess is generate by a seed word "sorea"
        by using probability of each letter in each position
    """
    seed_word = hack.get_seed_word()
    match_result = game.compare_guess_to_word(seed_word, wordle_word)
    print("Guess: 1", seed_word)
    print(match_result)

    hack.check_result(seed_word, match_result)
    print(hack.result_dict)

    hack.prune_word_list()
    print(hack.get_possible_word_dict())

    print("-------")
    match_record[1] = [seed_word, match_result]
    if game.check_win(match_result):
        print("You guessed it!")
    
    # """ 
    #     Second guess is generate by a seed word "sorea"
    #     by using probability of each letter in each position
    # """
    # second_word = "shock"
    # match_result = game.compare_guess_to_word(second_word, wordle_word)
    # print("Guess: 2", second_word)
    # print(match_result)

    # hack.check_result(second_word, match_result)
    # print(hack.result_dict)

    # hack.prune_word_list()
    # print(hack.get_possible_word_dict())

    # print("-------")
    # match_record[2] = [second_word, match_result]
    # if game.check_win(match_result):
    #     print("You guessed it!")
    

    """    
    All other guesses
    """   
    guess_count = 2
    match_flag = False
    while match_flag == False:
        print('Run guess:' + str(guess_count))
        guess_word = hack.generate_guess()
        match_result = game.compare_guess_to_word(guess_word, wordle_word)
        print("Guess: ",guess_word)
        print(match_result)

        hack.check_result(guess_word, match_result)
        print(hack.result_dict)

        hack.prune_word_list()
        print(hack.get_possible_word_dict())
        print("-------")
        match_record[guess_count] = [guess_word, match_result]

        guess_count += 1
        if game.check_win(match_result):
            print("You guessed it!")
            match_flag = True
            break

    print("Game end!")
    print(wordle_word)
    print(match_record)

    
if __name__ == "__main__":
    main()