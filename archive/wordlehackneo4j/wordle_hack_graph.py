"""
Wordle game hack with Neo4j
Author: Phat Doan
Date: 5/13/2022
"""

from wordle_game import WordleGame
from neo4j_conn import Neo4jConnection
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

    def __init__(self):
        """
            0: not matched alphabet
            1-5: position of the alphabet
                y: yellow (not matched position)
                g: green (matched position)
        """
        self.result = {1:{'y':[]
                         ,'g':""}
                      ,2:{'y':[]
                         ,'g':""}
                      ,3:{'y':[]
                         ,'g':""}
                      ,4:{'y':[]
                         ,'g':""}
                      ,5:{'y':[]
                         ,'g':""}
                      ,0:[]}

        rows = 3
        cols = 2
 
        self.markov_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

        self.SEED_WORD = "sorea"

    def get_result(self):
        return(self.result)

    def get_markov_matrix(self):
        return(self.markov_matrix)

    def get_seed_word(self):
        """
            Objective: return initial seed word
        """
        return(self.SEED_WORD)

    def check_result(self, guess, result):
        """
            Objective: check the latest guess and its result and store it in self.result
            args:
                guess:
                result
        """
        for i,r in enumerate(result):
            if r == 'g':
                if guess[i] != self.result[i+1]['g']:
                    self.result[i+1]['g'] = guess[i]
            elif r == 'y':
                if guess[i] not in self.result[i+1]['y']:
                    self.result[i+1]['y'].append(guess[i])
            else:
                if guess[i] not in self.result[0]:
                    self.result[0].append(guess[i])

    def create_cypher_query(self):
        """
            Objective: based on previous results, parse self.result to create a cypher query to retrieve a list of possible words
            
            return: string: cypher query
        """
        match_clause_list = []
        where_clause_list = []

        for i in range(1,6):
            if self.result[i]['g'] != "":
                match_clause_list.append(str("(w:Word)-[h"+str(i)+":HAS]->(a"+str(i)+":Alphabet)"))
                where_clause_list.append("(a"+str(i)+".alphabet = '" + self.result[i]['g']+"' and h"+str(i)+".relationship = '"+str(i)+"')")
            else:
                if self.result[i]['y']:
                    match_clause_list.append(str("(w:Word)-[h"+str(i)+":HAS]->(a"+str(i)+":Alphabet)"))
                    if len(self.result[i]['y']) == 1:
                        where_clause_list.append("(a"+str(i)+".alphabet = '" + self.result[i]['g']+"' and h"+str(i)+".relationship <> '"+str(i)+"')")
                    else:
                        in_clause = "['"
                        for y_alphabet in self.result[i]['y']:
                            in_clause += (y_alphabet +"','")

                        in_clause += "']"
                        where_clause_list.append("(a"+str(i)+".alphabet in" + in_clause + " and h"+str(i)+".relationship <> '"+str(i)+"')")
        
        if len(self.result[0])==1:
            match_clause_list.append("(w:Word)-[h0:HAS]->(a0:Alphabet)")
            where_clause_list.append("(a0.alphabet <> '" + self.result[0][0]+"' and h"+str(i)+".relationship <> '"+str(i)+"')")
        elif len(self.result[0]) > 1:
            match_clause_list.append("(w:Word)-[h0:HAS]->(a0:Alphabet)")
            in_clause = "['"
            for y_alphabet in self.result[0]:
                in_clause += (y_alphabet +"','")

            in_clause += "']"
            where_clause_list.append("NOT(a"+str(0)+".alphabet in" + in_clause + ")")

        cypher_query = "MATCH"

        for i, match_clause in enumerate(match_clause_list):
            if i == 0:
                cypher_query += match_clause
            else:
                cypher_query += (", " + match_clause)

        cypher_query += "WHERE"

        for i, where_clause in enumerate(where_clause_list):
            if i == 0:
                cypher_query += where_clause
            else:
                cypher_query += ("and " + where_clause)

        cypher_query += "return distinct w.word"
        return(cypher_query)
        # return([match_clause_list, where_clause_list])

    def get_neo4j_result(self, cypher_query):
        """
            Objective: use cypher query to get a list of possible words
        """
        conn = Neo4jConnection(uri="neo4j://localhost:7687", user="neo4j", pwd="neo4j")
        
        return (conn.query(cypher_query, db='neo4j'))


    def generate_guess(self, word_list):
        """
            For the second and third guesses, given a list of words from previous guesses, generate the next guess based on most frequently appears alphabet, accounting for result dictionary
            arg:
                word_list: list of possible words based on previous guesses
            return: a word
        """
        alphabet_dict = {'a':0
                        ,'b':1
                        ,'c':2
                        ,'d':3
                        ,'e':4
                        ,'f':5
                        ,'g':6
                        ,'h':7
                        ,'i':8
                        ,'j':9
                        ,'k':10
                        ,'l':11
                        ,'m':12
                        ,'n':13
                        ,'o':14
                        ,'p':15
                        ,'q':16
                        ,'r':17
                        ,'s':18
                        ,'t':19
                        ,'u':20
                        ,'v':21
                        ,'w':22
                        ,'x':23
                        ,'y':24
                        ,'z':25}

        guess =["_","_","_","_","_"]
        for i, g in enumerate(guess):
            if self.result[i+1]['g']:
                guess[i] = (self.result[i+1]['g'])
                self.markov_matrix[i][alphabet_dict[self.result[i+1]['g']]] = 1
            else: 
                

                # # remove yellow alphabet
                # for y in self.result[i+1]['y']:
                #     if y in alphabet:
                #         del alphabet[y]

                # # remove alphabet that are not in the guessed word
                # for not_exist in self.result[0]:
                #     if not_exist in alphabet:
                #         del alphabet[not_exist]

                # for word in word_list:
                #     alp_list = utils.convert_string_to_list(word)
                #     if alp_list[i] in alphabet:
                #         alphabet[alp_list[i]] += 1
                
                # guess[i] = (max(alphabet, key=alphabet.get))

                pass

        guess_word = ""

        for g in guess:
            guess_word += g

        return guess_word

def main():
    """
        Objective: run wordle
    """
    game = WordleGame()

    word = game.get_a_word()
    # word = "sorry"

    print("Let's play Worlde!")

    match_record = {}

    hack = WordleHack()

    ## First Guess
    seed_word = hack.get_seed_word()
    match_result = game.compare_guess_to_word(seed_word, word)
    print(seed_word)
    print(match_result)

    hack.check_result(seed_word, match_result)
    print(hack.result)

    match_record[1] = [seed_word, match_result]
    if game.check_win(match_result):
        print("You guessed it!")
    
    # Second and Third Guess
    for i in range(2,6):
        print('run ' + str(i))
        
        cypher_query = hack.create_cypher_query()

        print(cypher_query)

        neo4j_cypher_result = hack.get_neo4j_result(cypher_query)

        result_list = []
        for result in neo4j_cypher_result:
            result_list.append(result[0])

        guess_word = hack.generate_guess(result_list)
        print(guess_word)

        match_result = game.compare_guess_to_word(guess_word, word)
        print(match_result)

        hack.check_result(guess_word, match_result)
        print(hack.result)

        match_record[i] = [guess_word, match_result]
        if game.check_win(match_result):
            print("You guessed it!")
            break

    print("Game end!")
    print(word)
    print(match_record)

    
if __name__ == "__main__":
    main()