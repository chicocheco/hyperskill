from sys import exit
from random import randint


class TicTacToe:
    coordinates = {(1, 3): (0, 0), (2, 3): (0, 1), (3, 3): (0, 2),
                   (1, 2): (1, 0), (2, 2): (1, 1), (3, 2): (1, 2),
                   (1, 1): (2, 0), (2, 1): (2, 1), (3, 1): (2, 2)}

    def __init__(self):
        self.matrix = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.occupied_coords = set()

    def input_coords(self):
        while True:
            command = input('Enter the coordinates: ')
            args = command.split()
            if args[0] == 'exit':
                exit()
            else:
                a, b = (int(i) for i in args)
                if 0 < a < 4 and 0 < b < 4:
                    x, y = self.coordinates[a, b]
                    if self.is_free(x, y):  # else, continue while loop or exit
                        return x, y
                else:
                    print('Coordinates should be from 1 to 3!')

    def easy_coords(self):
        while True:
            x_rand, y_rand = (randint(0, 2) for _ in range(2))
            if (x_rand, y_rand) not in self.occupied_coords:
                print('Making move level "easy"')
                self.occupied_coords.add((x_rand, y_rand))
                return x_rand, y_rand

    def medium_coords(self, turn):
        winning_coords = set()
        for i, row in enumerate(self.matrix):
            if row.count(turn) == 2 and ' ' in row:
                winning_coords.add((i, row.index(' ')))

    def is_free(self, x, y):
        if (x, y) in self.occupied_coords:
            print('This cell is occupied! Choose another one!')
            return False
        self.occupied_coords.add((x, y))
        return True

    def menu(self):
        possible_args = ('user', 'easy')
        while True:
            try:
                command = input('Input command: ')
                args = command.split()
                if args[0].lower() == 'start' and args[1] in possible_args and args[2] in possible_args:
                    self.play(args[1], args[2])  # no need to know the second arg
                    break
                if args[0].lower() == 'exit':
                    exit()
            except ValueError:
                print('Bad parameters!')
            else:
                print('Bad parameters!')

    def play(self, player1, player2):
        self.print_matrix()
        human_turn = False  # computer starts
        if player1 == 'user':
            human_turn = True
        turn = 'X'
        while True:
            try:
                if human_turn:
                    x, y = self.input_coords()
                    self.matrix[x][y] = turn
                    if player2 != 'user':  # else human_turn = True
                        human_turn = False
                else:
                    x, y = self.easy_coords()
                    self.matrix[x][y] = turn
                    if player2 != 'easy':
                        human_turn = True
                self.print_matrix()
                if self.is_finished():
                    break
            except ValueError:
                print('You should enter numbers!')
                continue
            turn = 'O'

    def print_matrix(self):
        print('-' * 9, sep='')
        for i in range(len(self.matrix)):
            print(f"| {' '.join(self.matrix[i])} |")
        print('-' * 9)

    def is_finished(self):
        flat_matrix = [cell for cell in self.matrix for cell in cell]
        if any([self.horizontal(),
                self.vertical(),
                self.primary_diagonal(),
                self.secondary_diagonal()]):
            return True
        if ' ' not in flat_matrix:
            print('Draw')
            return True

    def horizontal(self):
        for row in self.matrix:
            set_row = set(row)
            if len(set_row) == 1 and ' ' not in set_row:
                print(f'{set_row.pop()} wins')  # horizontally
                return True

    def vertical(self):
        grid_90 = [cell for cell in zip(*self.matrix)]
        for row in grid_90:
            set_row = set(row)
            if len(set_row) == 1 and ' ' not in set_row:
                print(f'{set_row.pop()} wins')  # vertically
                return True

    def primary_diagonal(self):
        diag1 = {self.matrix[i][i] for i in range(len(self.matrix))}
        if len(diag1) == 1 and ' ' not in diag1:
            print(f'{diag1.pop()} wins')  # upper-left to lower-right
            return True

    def secondary_diagonal(self):
        n = len(self.matrix)
        diag2 = {self.matrix[i][j] for i in range(n) for j in range(n) if (i + j) == (n - 1)}
        if len(diag2) == 1 and ' ' not in diag2:
            print(f'{diag2.pop()} wins')  # upper-right to lower-left
            return True


if __name__ == '__main__':
    tictactoe = TicTacToe()
    tictactoe.menu()
