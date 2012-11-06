import re

word = list('hacker')

progress = list('_' * len(word))

bad_guesses = []

max_guesses = 6

def find_all(needle, haystack):
    return [m.start() for m in re.finditer(needle, haystack)]

while len(bad_guesses) < max_guesses:
    print "".join(progress)
    guess = raw_input('Guess a letter: ').lower()
    if guess in word:
        for i in find_all(guess, "".join(word)):
            progress[i] = guess
        if "_" not in progress:
            print "You won!"
            break
    else:
        bad_guesses.append(guess)
        print "Sorry, the letter %s is not in the word!" % guess

print "You lose"

