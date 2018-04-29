#!/usr/bin/env python3

# hangman game


import sys
import random


def main():
    while True:
        word_list = create_wordlist()
        word = get_word(word_list)
        print("\nPlay The", add_spaces("HANGMAN"), "Game\n")
        print("After 7 wrong guesses, the game is OVER.  GOOD LUCK!\n")
        play_game(word)
        choice = input("\nPlay again? [y/n] ")
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
                        word = line.upper()
                        word_list.append(word.replace("\n", ""))

        except FileNotFoundError:
            print("Word list not found, exiting program.")
            sys.exit()

        return word_list


def get_word(word_list):
    word = random.choice(word_list)
    return word


def get_letter():
    while True:
        letter = input("\nEnter a letter: ")
        if len(letter) == 1 and letter.isalpha():
            return letter.upper()
        else:
            print("That's not a letter, try again.")


def add_spaces(word):
    spaced_word = " ".join(word.upper())
    return spaced_word


def play_game(word):
    tried = ""
    guesses = 0
    wrong = 0
    word_line_list = ["_"] * len(word)
    char_list = ["_____", "|", "O", "\\", "|", "/", "|", "/", "\\"]
    draw_list = ([" "] * 10)
    is_wrong = False

    while wrong < 7:
        letter_index = 0
        i = 0

        draw_screen(word, is_wrong, tried, guesses, wrong, word_line_list, char_list, draw_list)

        letter = get_letter()

        if letter in tried:
            print("You already guessed that, try again.")
            is_wrong = False
            continue
        elif letter not in word:
            wrong += 1
            is_wrong = True
        else:
            is_wrong = False
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

        tried += letter
        guesses += 1

        if wrong > 6 and "_" in word_line_list:
            draw_screen(word, is_wrong, tried, guesses, wrong, word_line_list, char_list, draw_list)
            print("\n\nTHE WORD WAS:  ", word.upper())
        elif "_" not in word_line_list:
            draw_screen(word, is_wrong, tried, guesses, wrong, word_line_list, char_list, draw_list)
            print("\n*WINNER WINNER*\nYou guessed it in", guesses, "tries.")
            break


def draw_screen(word, is_wrong, tried, guesses, wrong, word_line_list, char_list, draw_list):
    draw_hangman(guesses, wrong, is_wrong, char_list, draw_list)

    print("-" * 72)

    i = 0
    while i < (len(word)):
        print(word_line_list[i], end=" ")
        i += 1

    print("{:>15} {:<3} {:>5} {:<3} {:>5} {:<3}".format("Guesses:", guesses, "Wrong:", wrong, "Tried:",
                                                        add_spaces(tried)))


def draw_hangman(guesses, wrong, is_wrong, char_list, draw_list):
    if is_wrong and wrong <= 7:
        draw_list.insert(wrong + 1, char_list[wrong + 1])

    if guesses == 0:
        draw_list = char_list
    elif wrong == 7:
        draw_list[2] = "{}\n     {}\n     {}\n     {}".format("|", "|", "|", "X")

    # use string format method to properly display the hangman pieces
    hangman = "{}\n     {}\n     {}\n    {}{}{}\n     {}\n     {}{}".format(char_list[0], char_list[1],
                                                                              draw_list[2], draw_list[3],
                                                                              draw_list[4], draw_list[5],
                                                                              draw_list[6], draw_list[7],
                                                                              draw_list[8])
    if wrong < 7:
        print(hangman)
    else:
        print(hangman)
        print("\n  {}\n\n".format("*UR DEAD*"))


if __name__ == "__main__":
    main()