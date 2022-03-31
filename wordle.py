# PYTHON WORDLE
# Necessary imports all part of the Standard lib. I renamed the functions imported to clarify what I have imported and
# to avoid collisions
from fileinput import input as file_input
from random import choice as ran_choice
from sys import exit as sys_exit

# Global messages to help translation. Every function has an m dict that stores the function messages to help
# translation
ALERT = "There isn't the file that stores the words. Please call 'python3 webScrap.py' to download it from GitHub"
INPUT = "Type your attempt: "
PLAY = "Let's play!"
STATE = "This is your guess number {} from {}"
GREAT = "Congratulations, You has solved the Wordle in {} attempts!"
SORRY = "You're out of attempts. Try to solve the Wordle again"
AGAIN = "Do you want to play again?"


# Given functions
def in_spot(letter: str):
    return f"\033[1m\033[42m\033[30m{letter.upper()}\033[0m"


def not_in_spot(letter: str):
    return f"\033[1m\033[43m\033[30m{letter.upper()}\033[0m"


def not_in_word(letter: str):
    return f"\033[1m\033[47m\033[30m{letter.upper()}\033[0m"


# Own functions
def word_intro() -> str:
    """
    Ask user for guess and check if it's a valid input

    Return:
        A string containing the word that the users has input.

    Parameters:
        No parameters.

    Exceptions:
        Any.

    """
   
    m = {
        "input": "Type your attempt: ",
        "notLen": "Your word hasn't the correct length, it have to be 5 letters long",
        "notWord": "Your input isn't a word, only words are allowed",
    }
    
    guess_ = input(m["input"])
    # Checking if word has 5 letters
    if len(guess_) != 5:
        print(m["notLen"])
        return word_intro()
    # Checking if input is composed by letters
    if not guess_.isalpha():
        print(m["notWord"])
        return word_intro()
    
    return guess_.lower()


def ask_user(question: str) -> bool:
    """
    A function that implements a yes/no question

    Return:
         a boolean (True/False)

    Parameters:
        question: the question you want the user answer


    Exceptions:
        Anything that user inputs that throw an error is parsed, shows error text and the execution continues.

    """
    
    m = {"notY": "Please enter a valid input"}
    
    if " (y/n): " not in question:
        question = question + " (y/n): "
    # Ask the user and do the manipulations on the str
    q = str(input(question)).lower()
    
    # This block tries to use the input to return True, False or asks the question again
    try:
        if q == 'y' or q == "yes":
            return True
        elif q == 'n' or q == "no":
            return False
        else:
            print(m["notY"])
            ask_user(question)
    except Exception as error:
        print(m["notY"])
        print(error)
        ask_user(question)


def check_game(guess_n: str, secret_: str) -> dict:
    """
    Function that checks how many letters the user has guessed
    Return:
         a dictionary composed by
            guess_n: a string containing the word properly formatted.
            solved_n: an integer with the completion state of the challenge

    Parameters:
        guess_n: the string that the user has input
        secret_: the word to solve

    Exceptions:
        Any

    """
    guess_r = ""
    solved_n = 0
    # for every letter in guess_n we check if is in spot, in word or isn't in word and returns the correct format
    for w, letter in enumerate(guess_n):
        if letter == secret_[w]:
            guess_r = guess_r + in_spot(letter)
            solved_n += 1
        elif letter in secret_:
            guess_r = guess_r + not_in_spot(letter)
        else:
            guess_r = guess_r + not_in_word(letter)
    
    return {"word": guess_r, "solved": solved_n}



if __name__ == '__main__':
    # Variables to customize tries and path to secrets
    tries = 6
    path = "secrets"

    # Importing the secrets from the file that is indicated in path to a list if exists, else trow an error and ends the
    # execution
    secrets = []
    try:
        with file_input(files=path) as f:
            for line in f:
                secrets.append(line)
    except OSError:
        sys_exit(ALERT)

    # Beginning of the game bucle, repeat is True until the end of the game where user can select to continue or
    # not. If the user selects don't continue repeat is set to False and ends the bucle.
    repeat = True
    while repeat:
        secret = ran_choice(secrets)
        print(PLAY)
        solved = 0
        for i in range(6):
            # If solved equals 5 all letters are in place, and we have to break the bucle congratulating the user
            if solved == 5:
                print(GREAT.format(i+1))
                break
            print(STATE.format(i+1, tries))
            guess = word_intro()
            result = check_game(guess, secret)
            solved = result["solved"]
            print(result["word"])

        # Ending the bucle if solved is not 5 the program prints message to tell the user that has lost.
        if solved != 5:
            print(SORRY)
            
        # The program asks if user wants to continue (y/n)
        repeat = ask_user(AGAIN)
