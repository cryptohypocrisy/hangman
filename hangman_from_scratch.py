#!/usr/bin/env python3

# hangman game


import sys
import random
import copy as c


def main():
    while True:
        word_list = create_wordlist()
        word = get_word(word_list)
        print("\nPlay The", add_spaces("HANGMAN"), "Game!")
        play_game(word)
        choice = input("Play again? [y/n] ")
        if choice.lower() == 'y':
            print("Choice =", choice.lower())
            continue
        else:
            break

    print("\nThank's for playing :))))")


def create_wordlist():
    word_list = []

    while True:
        try:
            file_path = 'wordlist.txt'
            with open(file_path) as file:
                for line in file:
                    if line != "\n":
                        word = line.lower()
                        word_list.append(word.replace("\n", ""))

        except FileNotFoundError:
            print("Word list not found, exiting program.")
            sys.exit()

        return word_list


def get_word(word_list):
    word = random.choice(word_list)
    return word


def get_letter(tried_list):
    while True:
        letter = input("\nEnter a letter: ")
        if len(letter) == 1 and letter.isalpha():
            return letter
        else:
            print("That's not a letter, try again.")


def add_spaces(word):
    spaced_word = " ".join(word)
    return spaced_word


def play_game(word):
    tried_list = []
    guesses = 0
    wrong = 0
    i = 0
    word_line_list = ["_"] * len(word)
    char_list = ["_____", "|", "O", "\\", "|", "/", "|", "/", "\\"]
    mod_char_list = ([" "] * 10)
    guess_wrong = False

    while wrong < 10:
        letter_index = 0
        i = 0

        draw_screen(word, guess_wrong, tried_list, guesses, wrong, word_line_list, char_list, mod_char_list, letter="")

        letter = get_letter(tried_list)

        if letter in tried_list:
            print("You already guessed that, try again.")
            guess_wrong = False
            continue
        elif letter not in word:
            wrong += 1
            guess_wrong = True
        else:
            guess_wrong = False
            if word.count(letter) > 1:
                while i < word.count(letter):
                    letter_index = word.find(letter, letter_index + i)
                    word_line_list.pop(letter_index)
                    word_line_list.insert(letter_index, letter)
                    i += 1
            else:
                letter_index = word.find(letter)
                word_line_list.pop(letter_index)
                word_line_list.insert(letter_index, letter)

        tried_list.append(letter)
        guesses += 1
        if wrong > 9 and "_" in word_line_list:
            draw_screen(word, guess_wrong, tried_list, guesses, wrong, word_line_list, char_list, mod_char_list, letter="")
            print("\nYOU LOSE\n\nTHE WORD WAS:\t", word)
        elif "_" not in word_line_list:
            draw_screen(word, guess_wrong, tried_list, guesses, wrong, word_line_list, char_list, mod_char_list, letter="")
            print("\nYou guessed it in", guesses, "tries.")
            break


def draw_screen(word, guess_wrong, tried_list, guesses, wrong, word_line_list, char_list, mod_char_list, letter):
    tried = ""
    for letter in tried_list:
        tried += (letter.upper() + " ")

    draw_hangman(guesses, wrong, guess_wrong, char_list, mod_char_list)

    print("-" * 64)

    i = 0
    while i < (len(word)):
        print(word_line_list[i], end=" ")
        i += 1

    print("{:>15} {:<3} {:>5} {:<3} {:>5} {:<3}".format("Guesses:", guesses, "Wrong:", wrong, "Tried:", tried))


def draw_hangman(guesses, wrong, guess_wrong, char_list, mod_char_list):
    if guess_wrong:
        try:
            mod_char_list.insert(wrong - 1, char_list[wrong - 1])
        except IndexError:
            pass

    if guesses == 0:
        mod_char_list = char_list

    hangman = "{}\n     {}\n     {}\n    {}{}{}\n     {}\n     {}{}".format(mod_char_list[0], mod_char_list[1],
                                                                              mod_char_list[2], mod_char_list[3],
                                                                              mod_char_list[4], mod_char_list[5],
                                                                              mod_char_list[6], mod_char_list[7],
                                                                              mod_char_list[8])

    print(hangman)


if __name__ == "__main__":
    main()