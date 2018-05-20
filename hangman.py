#!/usr/bin/env python3

# hangman game


import sys  # used for sys.exit()
import random  # use random.choice() to pick random word from word_list


# create word_list, get word from word_list, print title and rules, call play_game() and
# use loop for repeated play
def main():
    while True:  # loop for play again
        word_list = create_wordlist()  # get the word_list from wordlist.txt
        word = get_word(word_list)  # pick a random word from wordlist.txt

        print("\nPlay The", add_spaces("HANGMAN"), "Game\n")
        print("After 7 wrong guesses, the game is OVER.  GOOD LUCK!\n")

        play_game(word)  # start the game

        choice = input("\nPlay again? [y/n] ")  # see if user wants to play again

        if choice.lower() == 'y':
            print("Choice =", choice.lower())
            continue
        else:
            break  # user doesn't want to play again, end program

    print("\nThanks for playing :))))")


# create and return word_list from wordlist.txt file
def create_wordlist():
    word_list = []

    while True:
        try:
            file_path = 'wordlist.txt'
            with open(file_path) as file:
                for line in file:
                    if line != "\n":  # this is specific to word lists that have empty lines between words
                        word = line.upper()
                        word_list.append(word.replace("\n", ""))
        except FileNotFoundError:
            print("Word list not found, exiting program.")
            sys.exit()  # exit if we can't find the wordlist

        return word_list


# use choice method in random module to return a random word
def get_word(word_list):
    word = random.choice(word_list)
    return word


# get user's letter guess
def get_letter():
    while True:
        letter = input("\nEnter a letter: ")
        if len(letter) == 1 and letter.isalpha():  # if input is more than one character or contains anything
                                                   # other than letters, force user to enter guess again
            return letter.upper()
        else:
            print("That's not a letter, try again.")


# take any string as input and insert spaces between letters and capitalize
def add_spaces(word):
    spaced_word = " ".join(word.upper())
    return spaced_word


# workhorse function; initializes all important variables and calls other functions to get user's guess
# and draw the screen
def play_game(word):
    tried = ""
    num_guesses = 0
    num_wrong = 0
    word_line_list = ["_"] * len(word)  # this list is printed in draw_screen() and contains underscore placeholders for
                                        # the word chosen in get_word(); as the user guesses correctly, the
                                        # correct letters are inserted into this list in place of the underscore
                                        # placeholders
    symb_list = ["_____", "|", "O", "\\", "|", "/", "|", "/", "\\"]  # this list contains the symbols that make
                                                                     # up the hangman figure; they are incrementally
                                                                     # inserted into draw_list as the number
                                                                     # of wrong guesses increases
    draw_list = ([" "] * 9)  # this list is used as an empty placeholder for the hangman pieces;  they are
                              # inserted into this list as the number of wrong guesses increases
    is_wrong = False  # used to tell draw_hangman() whether to insert the next piece of the hangman (symb_list)
                      # into draw_list

    while num_wrong < 7:  # execute this loop until user has made 7 wrong guesses
        letter_index = 0  # holds index of a found letter, used with pop() and find()
        i = 0  # used to increment the while loop that looks for multiples of the same letter

        draw_screen(is_wrong, tried, num_guesses,   # drag hangman and play area
                    num_wrong, word_line_list,
                    symb_list, draw_list)

        letter = get_letter()  # get a guess from the user

        if letter in tried:  # input validation for repeat guesses
            print("You already guessed that, try again.")
            is_wrong = False
            continue
        elif letter not in word:  # guess is wrong, increment number of wrong guesses and set is_wrong=True
            num_wrong += 1
            is_wrong = True
        else:
            is_wrong = False  # letter has been found, if there is more than one instance of letter, loop to find it
            if word.count(letter) > 1:
                while i < word.count(letter):
                    letter_index = word.find(letter, letter_index + 1)  # find the index of the instance
                    word_line_list.pop(letter_index)  # pop the underscore placeholder
                    word_line_list.insert(letter_index, letter)  # insert the correctly guessed letter into popped index
                    i += 1  # increments to end the loop after we've found all instances of the letter
            else:
                letter_index = word.find(letter)
                word_line_list.pop(letter_index)
                word_line_list.insert(letter_index, letter)

        tried += letter  # add the guessed letter into the string containing tried letters
        num_guesses += 1  # increment number of guesses to display in draw_screen()

        if num_wrong > 6 and "_" in word_line_list:  # if user is on their 7th guess and there are still
                                                     # underscore placeholders in word_line_list, end the game
                                                     # and draw the screen one more time
            draw_screen(is_wrong, tried, num_guesses, num_wrong, word_line_list, symb_list, draw_list)
            print("\n\nTHE WORD WAS:  ", word.upper())  # reveal hidden word
        elif "_" not in word_line_list:  # if all placeholders have been replaced with letters, the word has
                                         # been guessed; end the game, draw the screen, and tell the user they've won
            draw_screen(is_wrong, tried, num_guesses, num_wrong, word_line_list, symb_list, draw_list)
            print("\n*WINNER WINNER*\nYou guessed it in", num_guesses, "tries.")
            break


# draws the hangman and the rest of the play area including the statistics
def draw_screen(is_wrong, tried, num_guesses, num_wrong, word_line_list, symb_list, draw_list):

    draw_hangman(num_guesses, num_wrong, is_wrong, symb_list, draw_list)  # call draw_hangman to
                                                                          # print the hangman figure

    print("-" * 72)  # print the divider line that separates hangman figure from the rest of draw_screen

    for letter in word_line_list:  # print the letters/underscore placeholders for the secret word
        print(letter, end=" ")

    print("{:>15} {:<3} {:>5} {:<3} {:>5} {:<3}".format("Guesses:", num_guesses, "Wrong:", num_wrong, "Tried:",
                                                        add_spaces(tried)))  # display statistics


# draws the hangman figure differently depending on function arguments
def draw_hangman(num_guesses, num_wrong, is_wrong, symb_list, draw_list):
    if is_wrong and num_wrong <= 7:
        draw_list.insert(num_wrong + 1, symb_list[num_wrong + 1])  # if the user guesses wrong, take the hangman
                                                                   # piece from symb_list and insert incrementally
                                                                   # into indices 2-8 in draw_list, which is what will
                                                                   # be used below to print the hangman; indexes 0-1
                                                                   # will be drawn directly by symb_list because they
                                                                   # form the base of the gallows and will always be
                                                                   # printed

    if num_guesses == 0:  # if it's the first time printing the screen (i.e. title screen), print the whole hangman
        draw_list = symb_list
    elif num_wrong == 7:  # if the user has made their last wrong guess and the game is over, print
                          # a modified version of the hangman figure where he's been dropped
        draw_list[2] = "{}\n     {}\n     {}\n     {}".format("|", "|", "|", "X")

    # use string format method to properly display the hangman pieces; draw_list indices are empty and print
    # nothing until wrong guesses insert symbols from symb_list
    hangman = "{}\n     {}\n     {}\n    {}{}{}\n     {}\n     {}{}".format(symb_list[0], symb_list[1],
                                                                              draw_list[2], draw_list[3],
                                                                              draw_list[4], draw_list[5],
                                                                              draw_list[6], draw_list[7],
                                                                              draw_list[8])

    if num_wrong < 7:
        print(hangman)  # print hangman figure for normal turns
    else:
        print(hangman)
        print("\n  {}\n".format("*UR DEAD*"))  # print a special message if the user has made their
                                                 # last wrong guess and the game is over


if __name__ == "__main__":  # if not imported as a module, run the main() function
    main()
