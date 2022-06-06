"""
Objective: to simulate results from wordle game and test efficacy and accuracy of world_hack algorithm

"""


from statistics import median
from wordle_hack import WordleHack
from wordle_game import WordleGame
import numpy as np

def main(simulation_run = 100):
    """
        Objective: run wordle simulation
    """
    print("Running wordle game simulation")
    result_dict = {}
    result_guess_count_list = []
    for i in range(0,simulation_run):
        game = WordleGame()
        wordle_word = game.get_a_word()
        match_record = {}
        hack = WordleHack()
        """ 
            Initiate guess is generate by a seed word "sorea"
            by using probability of each letter in each position
        """
        seed_word = hack.get_seed_word()
        match_result = game.compare_guess_to_word(seed_word, wordle_word)
        hack.check_result(seed_word, match_result)
        hack.prune_word_list()
        match_record[1] = [seed_word, match_result]
        if game.check_win(match_result):
            next
        
        # """ 
        # Second guess is generate by a seed word "sorea"
        # by using probability of each letter in each position
        # """
        # second_word = "shock"
        # match_result = game.compare_guess_to_word(second_word, wordle_word)
        # hack.check_result(second_word, match_result)
        # hack.prune_word_list()
        # match_record[2] = [second_word, match_result]

        """    
        All other guesses
        """   
        guess_count = 2
        match_flag = False
        while match_flag == False:
            guess_word = hack.generate_guess()
            match_result = game.compare_guess_to_word(guess_word, wordle_word)
            hack.check_result(guess_word, match_result)            
            hack.prune_word_list()
            match_record[guess_count] = [guess_word, match_result]
            guess_count += 1
            if game.check_win(match_result):
                match_flag = True
                break
    
        result_dict[i] = {wordle_word: guess_count}

        result_guess_count_list += [guess_count]
    print("simulation complete")
    print(result_dict)

    print("Total simulation run: ", simulation_run)
    print("Least guess count: ", np.min(result_guess_count_list))
    print("Most guess count: ", np.max(result_guess_count_list))
    print("Average guess count: ", np.mean(result_guess_count_list))
    print("Median guess count: ", np.median(result_guess_count_list))
    print("Standard deviation guess count: ", np.std(result_guess_count_list))
    print("Total runs with 6 or less guesses: ", len(list(filter(lambda num: num <=6, result_guess_count_list))))

if __name__ == "__main__":
    main()