from wordle_hack import WordleHack
from wordle_game import WordleGame

def check_result_input():
    result_flag = False
    while result_flag == False:
        match_result = input("Enter the result of the guess: ")

        result_count = 0
        for r in match_result:
            if r in ['_','y','g']:
                result_count += 1
        
        if len(match_result) == 5 and result_count == 5:
            result_flag = True

    return(match_result)

def main():
    """
        Objective: run wordle
    """
    print("Let's hack Worlde!")

    TOTAL_GUESS_COUNT = 6

    game = WordleGame()
    hack = WordleHack()
    match_record = {}
    guess_count_flag = False
    while guess_count_flag == False:
        guess_count_to_now = input("How many guess(es) have you done? ")
        if int(guess_count_to_now):
            guess_count_flag = True

    guess_count_to_now = int(guess_count_to_now)
    for i in range(0, guess_count_to_now):
        guess_word = game.get_input("Enter your guess:")
        match_result = check_result_input()
        hack.check_result(guess_word, match_result)
        hack.prune_word_list()
        match_record[i] = [guess_word, match_result]

    print(match_record)
    print("-------")
    print("Remaining possible words: ", hack.get_possible_word_dict().keys())

    game_over_flag = False
    for i in range(guess_count_to_now, TOTAL_GUESS_COUNT):
        guess_word = hack.generate_guess()
        print("Suggested next guess is: ", guess_word)
        
        guess_correct_check_flag = False
        while guess_correct_check_flag == False:
            guess_correct_bool = input("Is the guess correct? ")
            if guess_correct_bool in ['y','n','Y','N']:
                guess_correct_check_flag = True

        if guess_correct_bool in ['Y','y']:
            game_over_flag = True
            print("Congrats! The Wordle word is: ", guess_word)
            match_record[i] = [guess_word, "ggggg"]
            break
        else:
            match_result = check_result_input()
            hack.check_result(guess_word, match_result)
            hack.prune_word_list()
            match_record[i] = [guess_word, match_result]
        
        print(match_record)
        print("Remaining possible words: ", hack.get_possible_word_dict().keys())
        print("-------")

    if game_over_flag == False:
        print("Better luck next time!")

    print("Match record:")
    print(match_record)


if __name__ == "__main__":
    main()