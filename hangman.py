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

    def game_status(self):
        if len(self.incorrect) >= Game.MAX_GUESSES:
            self.gameover = True
            return "\nYou lose. The word was %r." % self.word
        if set(self.correct) == set(self.word):
            self.gameover = True
            return "\nYou won!"
        return "" 

    def game_string(self, status=""):
        result = "\n" + "=" * 30 + "\n"
        result += Game.HANGMAN_STRINGS[len(self.incorrect)]
        result += "\nIncorrect guesses: %s" % ", ".join(self.incorrect)
        result += "\nProgress: %s" % self.get_progress()
        result += status
        return result

#-------------------------------------------------------------------------------
def valid_guess(game):
    while True:
        guess = raw_input("Guess a letter: ").lower()
        if len(guess) > 1 or guess not in string.lowercase:
            print "Please guess a letter."
        elif game.already_guessed(guess):
            print "You've already guessed %r." % guess
        else:
           return guess

if __name__ == "__main__":
    keepGoing = True
    while keepGoing:
        game = Game()
        print "WELCOME TO HANGMAN"
        print game.game_string()
        while not game.gameover:
            guess = valid_guess(game)
            game.guess_letter(guess)
            status = game.game_status()
            print game.game_string(status)
        play_again = raw_input("Play again? (y/n): ").lower()
        if "n" in play_again:
            keepGoing = False
    print "Thanks for playing!" 
