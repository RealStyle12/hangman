import re
from random import choice

def random_word():
    dictionary = open('dictionary.txt', 'r').readlines()
    words = [word.strip() for word in dictionary]
    return choice(words)

def find_all(needle, haystack):
    return [m.start() for m in re.finditer(needle, haystack)]

def update_progress(guess):
    for i in find_all(guess, word):
        progress[i] = guess

word = random_word()
progress = list('_' * len(word))
bad_guesses = []
max_guesses = 6
gameover = False

while not gameover:
    print "".join(progress)
    guess = raw_input('Guess a letter: ').lower()
    if guess in bad_guesses or guess in progress:
        print "You've already guessed %s" % guess
    elif guess in word:
        update_progress(guess)
        if "_" not in progress:
            print "You won! The word was %s" % word
            gameover = True
    else:
        bad_guesses.append(guess)
        print "Sorry, the letter %s is not in the word!" % guess
        if len(bad_guesses) >= max_guesses:
            print "You lose. The word was %s" % word
            gameover = True

