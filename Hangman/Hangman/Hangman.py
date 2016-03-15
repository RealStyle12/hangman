import string
from random import choice

class Game():
    MAX_GUESSES = 6
    incorrect = []
    correct = []
    


    def random_word():
        dictionary = open('dictionary.txt', 'r').readlines()
        words = [word.strip() for word in dictionary]
        return choice(words)

    word = random_word()

    def get_progress(self):
        return "".join([let if let in Game.correct else "_" for let in Game.word])

    def __init__(self):
        self.LocalIncorectNumber = 0
        self.progress = self.get_progress()
        self.gameover = False

    def already_guessed(self, guess):
        return guess in Game.correct + Game.incorrect

    def guess_letter(self, guess):
        if guess in Game.word:
            Game.correct.append(guess)
        else:
            Game.incorrect.append(guess)
            self.LocalIncorectNumber=self.LocalIncorectNumber+1;

    def status(self):
        if self.LocalIncorectNumber >= Game.MAX_GUESSES:
            self.gameover = True
            return "\nYou lose. The word was %r." % Game.word
        if set(Game.correct) == set(Game.word):
            self.gameover = True
            return "\nYou won!"
        return "" 

    def __str__(self):
        result = "\n" + "=" * 30 + "\n"
        result = "\n" +"Number of guesses: " + str(Game.MAX_GUESSES - self.LocalIncorectNumber)
        result += "\nIncorrect guesses: %s" % ", ".join(Game.incorrect)
        result += "\nProgress: %s" % self.get_progress()
        result += self.status()
        return result

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
        print game
        while not game.gameover:
            guess = valid_guess(game)
            game.guess_letter(guess)
            print game
        play_again = raw_input("Play again? (y/n): ").lower()
        if "n" in play_again:
            keepGoing = False
    print "Thanks for playing!" 
