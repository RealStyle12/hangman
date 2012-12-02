Console-based Hangman game in [Python](http://www.python.org), with a smidge of networking.

Written during [Hacker School](https://www.hackerschool.com/), Batch[4], Fall 2012.

## Hangman
### Rules
- Words randomly chosen from `dictionary.txt`
- Guess 1 letter at a time
- 6 incorrect guesses ends the game

###Usage
Run this command:

    python hangman.py

A sample game. Can you guess the answer?

            -----
            |   |
            O   |
           /|\  |
                |
                |
            ---------

    Incorrect guesses: a, o, s, i
    Progress: _unner
    Guess a letter:

In case you were wondering, it was `dunner`.

## Smidge of Networking
This is hardly a networking game. You can run `server.py` and have multiple clients playing via `client.py`. Unfortunately, it is still single player. Haven't come up with a fun way to make it multi-player yet... suggestions welcome!

## Acknowledgements
Thanks to Nick from HS for helping me get started, working out the server/client state machine logic, and refactoring :)
