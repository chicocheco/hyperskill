import random
from collections import deque
from pathlib import Path

"""
input: 
rock,gun,lightning,devil,dragon,water,air,paper,sponge,wolf,tree,human,snake,scissors,fire

problem: 
get all 7 preceding choices of e.g. 'water'

solution:
shift all choices with deque.rotate() to the right so they appear at indices 0-6

example:
water beats: dragon, devil, lightning, gun, rock, | fire, scissors
"""

choices = deque(['scissors', 'rock', 'paper'])
initiated = False
content, player_name, f = None, None, None
lino, score = 0, 0
while True:
    if not initiated:
        player_name = input('Enter your name: ')
        if player_name == '!exit':
            print('Bye!')
            break
        else:
            print(f'Hello, {player_name}')
            filename = Path('rating.txt')
            filename.touch(exist_ok=True)  # will create file, if it exists will do nothing

            f = open(filename, 'r+')  # read without truncating
            content = f.readlines()
            for i, line in enumerate(content):
                if line.startswith(player_name):
                    score = int(line.split()[1])
                    lino = i
                    break
        inp_options = input()
        if inp_options:
            choices = deque(inp_options.split(','))
        print("Okay, let's start")
        initiated = True

    choice = input()
    comp_choice = random.choice(choices)
    if choice == '!exit':
        print('Bye!')
        f.writelines(content)
        f.close()
        break
    if choice == '!rating':
        for line in content:
            print(line)
        continue
    if choice not in choices:
        print('Invalid input')
        continue

    # now evaluate choices:
    if choice == comp_choice:
        score += 50
        print(f'There is a draw ({choice})')
    else:  # get beaten choices
        half_opts = len(choices) // 2
        ix_choice = choices.index(choice)
        choices.rotate(half_opts - ix_choice)  # shift all to the right so we get first 7 choices at indices 0-6
        beaten_chces = [choices[i] for i in range(half_opts)]
        if comp_choice in beaten_chces:  # computer is beaten
            score += 100
            print(f'Well done. The computer chose {comp_choice} and failed')
        else:
            print(f'Sorry, but the computer chose {comp_choice}')

    if content:
        content[lino] = f'{player_name} {score}'  # preserve order
    else:
        content = [f'{player_name} {score}']
