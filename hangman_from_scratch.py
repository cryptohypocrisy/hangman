#!/usr/bin/env python3

# hangman game


import sys
import random


def main():
    word_list = create_wordlist()
    word = get_word(word_list)
    print("Play The", add_spaces("HANGMAN"), "Game!")
    play_game(word)
    


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
        letter = input("Enter a letter: ")
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
    i = 1
    word_line_list = ["_"] * len(word)

    while True:
        letter_index = 0

        draw_screen(word, tried_list, guesses, wrong, word_line_list, letter="")

        letter = get_letter(tried_list)

        if letter in tried_list:
            print("You already guessed that, try again.")
            continue
        elif letter not in word:
            wrong += 1
        else:
            if word.count(letter) > 1:
                while i <= word.count(letter):
                    letter_index = word.find(letter, letter_index+1)
                    word_line_list.pop(letter_index)
                    word_line_list.insert(letter_index, letter)
                    i += 1
            else:
                letter_index = word.find(letter)
                word_line_list.pop(letter_index)
                word_line_list.insert(letter_index, letter)
       
        tried_list.append(letter)
        guesses += 1


def draw_screen(word, tried_list, guesses, wrong, word_line_list, letter):
   
    tried = ""
    for letter in tried_list:
        tried += (letter.upper() + " ")
    print("-" * 64)

    i = 0
    while i < (len(word)):
        print(word_line_list[i], end=" ")
        i += 1
            
    print("{:>15} {:<3} {:>5} {:<3} {:>5} {:<3}".format("Guesses:", guesses, "Wrong:", wrong, "Tried:", tried))

    


if __name__ == "__main__":
    main()
