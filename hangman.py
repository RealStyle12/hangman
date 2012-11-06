import string
import re
from random import choice

MAX_GUESSES = 6
HANGMAN_STRINGS = [
            """
                    -----
                    |   |
                        |
                        |
                        |
                        |
                    ---------
            """,
            """
                    -----
                    |   |
                    O   |
                        |
                        |
                        |
                    ---------
            """,

            """
                    -----
                    |   |
                    O   |
                    |   |
                        |
                        |
                    ---------
            """,
            """
                    -----
                    |   |
                    O   |
                    |\  |
                        |
                        |
                    ---------
            """,
            """
                    -----
                    |   |
                    O   |
                   /|\  |
                        |
                        |
                    ---------
            """,
            """
                    -----
                    |   |
                    O   |
                   /|\  |
                     \  |
                        |
                    ---------
            """,
            """
                    -----
                    |   |
                    O   |
                   /|\  |
                   / \  |
                        |
                    ---------
            """]

def random_word():
    dictionary = open('dictionary.txt', 'r').readlines()
    words = [word.strip() for word in dictionary]
    return choice(words)

def get_progress(correct, word):
    return "".join([let if let in correct else "_" for let in word])

if __name__ == "__main__":
    incorrect = []
    correct = []
    gameover = False

    word = random_word()

    while not gameover:
        print HANGMAN_STRINGS[len(incorrect)]
        print "Incorrect guesses: %s" % ", ".join(incorrect)
        print "Progress: %s" % get_progress(correct, word)

        while True:
            guess = raw_input('Guess a letter: ').lower()
            if len(guess) > 1 or guess not in string.lowercase:
                print "Please guess a letter"
            elif guess in correct + incorrect:
                print "You've already guessed %s" % guess
            else:
                break

        if guess in word:
            correct.append(guess)
        else:
            incorrect.append(guess)

        if len(incorrect) >= MAX_GUESSES:
            print "You lose. The word was %s" % word
            gameover = True
        if set(correct) == set(word):
            print "You won! The word was %s" % word
            gameover = True
