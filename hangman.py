import random
from string import ascii_lowercase

print('H A N G M A N')

while True:
    answer = input('Type "play" to play the game, "exit" to quit: ')
    if answer == 'exit':
        break
    if answer != 'play':
        continue
    target = random.choice(['python', 'java', 'kotlin', 'javascript'])
    letters = set(target)
    used = set()
    guessed = ['-'] * len(target)
    attempts = 8
    while attempts > 0:
        str_guessed = ''.join(guessed)
        if str_guessed == target:
            print('You guessed the word!\nYou survived!')
            break
        print('\n', str_guessed)
        guess = input('Input a letter: ')
        if len(guess) != 1:
            print('You should input a single letter')
            continue
        if guess not in ascii_lowercase:
            print('It is not an ASCII lowercase letter')
            continue
        if guess in used:
            print('You already typed this letter')
            continue
        if guess in letters:
            indexes = [i for i, letter in enumerate(target) if letter == guess]
            for i in indexes:
                guessed[i] = guess
        else:
            print('No such letter in the word')
            attempts -= 1
        used.add(guess)
    else:
        print('You are hanged!')

