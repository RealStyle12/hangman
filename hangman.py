import string
from random import choice

class Game():
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

    def __init__(self):
        self.word = self.random_word()
        self.incorrect = []
        self.correct = []
        self.progress = self.get_progress()
        self.gameover = False

    def random_word(self):
        dictionary = open('dictionary.txt', 'r').readlines()
        words = [word.strip() for word in dictionary]
        return choice(words)

    def get_progress(self):
        return "".join([let if let in self.correct else "_" for let in self.word])

    def already_guessed(self, guess):
        return guess in self.correct + self.incorrect

    def guess_letter(self, guess):
        if guess in self.word:
            self.correct.append(guess)
        else:
            self.incorrect.append(guess)

    def game_over(self):
        if len(self.incorrect) >= Game.MAX_GUESSES:
            self.gameover = True
            return True
        return False

    def game_won(self):
        if set(self.correct) == set(self.word):
            self.gameover = True
            return True
        return False

    def game_string(self):
        result = "=" * 30 + "\n"
        result += Game.HANGMAN_STRINGS[len(self.incorrect)]
        if self.game_won():
            result += "\nYou won! The word was %r" % self.word
        elif len(self.incorrect) < Game.MAX_GUESSES:
            result += "\nIncorrect guesses: %s" % ", ".join(self.incorrect)
            result += "\nProgress: %s" % self.get_progress()
        elif self.game_over():
            result += "\nYou lose. The word was %s" % self.word
        return result

if __name__ == "__main__":
    game = Game()
    print game.game_string()
    while not game.gameover:
        while True:
            guess = raw_input("Guess a letter: ").lower()
            if len(guess) > 1 or guess not in string.lowercase:
                print "Please guess a letter."
            elif game.already_guessed(guess):
                print "You've already guessed %r." % guess
            else:
                break

        game.guess_letter(guess)
        print game.game_string()
