from sys import exit
from random import randint


class TicTacToe:
    coordinates = {(1, 3): (0, 0), (2, 3): (0, 1), (3, 3): (0, 2),
                   (1, 2): (1, 0), (2, 2): (1, 1), (3, 2): (1, 2),
                   (1, 1): (2, 0), (2, 1): (2, 1), (3, 1): (2, 2)}

    def __init__(self):
        self.matrix = [[' ', ' ', ' '] for _ in range(3)]
        self.occupied_coords = set()

    def input_coords(self):
        while True:
            try:
                command = input('Enter the coordinates: ')
                args = command.split()
                if args[0] == 'exit':
                    exit()
                else:
                    a, b = (int(i) for i in args)
                    if 0 < a < 4 and 0 < b < 4:
                        x, y = self.coordinates[a, b]  # get indexes
                        if self.is_free(x, y):  # else, continue while loop or exit
                            return x, y
                    else:
                        print('Coordinates should be from 1 to 3!')
            except ValueError:
                print('You should enter numbers!')

    def is_free(self, x, y):
        if (x, y) in self.occupied_coords:
            print('This cell is occupied! Choose another one!')
            return False
        self.occupied_coords.add((x, y))
        return True

    def easy_coords(self):
        while True:
            x_rand, y_rand = (randint(0, 2) for _ in range(2))
            if (x_rand, y_rand) not in self.occupied_coords:
                self.occupied_coords.add((x_rand, y_rand))
                return x_rand, y_rand

    def win_horizontally(self, turn):
        for i, row in enumerate(self.matrix):
            if row.count(turn) == 2 and ' ' in row:
                self.occupied_coords.add((i, row.index(' ')))
                return i, row.index(' ')  # horizontal
        return None

    def win_vertically(self, turn):
        column = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                column.append(self.matrix[j][i])
                if j == 2:
                    if column.count(turn) == 2 and ' ' in column:
                        self.occupied_coords.add((column.index(' '), i))
                        return column.index(' '), i  # vertical
                    column.clear()
        return None

    def win_primary_diagonal(self, turn):
        diag1 = [self.matrix[i][i] for i in range(len(self.matrix))]
        if diag1.count(turn) == 2 and ' ' in diag1:
            x = diag1.index(' ')
            self.occupied_coords.add((x, x))
            return x, x  # primary diagonal
        return None

    def win_secondary_diagonal(self, turn):
        n = len(self.matrix)
        diag2 = [(i, j, self.matrix[i][j]) for i in range(n) for j in range(n) if (i + j) == (n - 1)]
        values = [i[2] for i in diag2]
        if values.count(turn) == 2 and ' ' in values:
            for x, y, v in diag2:
                if v == ' ':
                    self.occupied_coords.add((x, y))
                    return x, y  # secondary diagonal
        return None

    def medium_coords(self, turn):
        """
        Stage 4/5
        1. If it can win in one move (if it has two in a row), it places a third to get three in a row and win.
        2. If the opponent can win in one move, it plays the third itself to block the opponent to win.
        3. Otherwise, it makes a random move.
        """
        for t in ('O' if turn == 'X' else 'X'):
            for possible_win in (self.win_horizontally, self.win_vertically,
                                 self.win_primary_diagonal, self.win_secondary_diagonal):
                coords = possible_win(t)
                if coords is not None:
                    return coords
        return self.easy_coords()  # defaults to this when there are no potential win lines:

    def hard_coords(self, turn):
        n = len(self.matrix)
        best_score = -99999
        best_move = None
        for i in range(n):
            for j in range(n):
                if self.matrix[i][j] == ' ':
                    self.matrix[i][j] = turn  # always ai
                    score = self.minimax(0, False, turn)
                    self.matrix[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = i, j
        x, y = best_move
        self.occupied_coords.add((x, y))
        return x, y

    def minimax(self, depth, is_maximizing, turn):
        opponent = 'O' if turn == 'X' else 'X'
        scores = {turn: 10,
                  opponent: -10,
                  'draw': 0}
        result = self.evaluate()
        if result is not None:
            return scores[result]

        n = len(self.matrix)
        if is_maximizing:
            best_score = -99999
            for i in range(n):
                for j in range(n):
                    if self.matrix[i][j] == ' ':
                        self.matrix[i][j] = turn
                        score = self.minimax(depth + 1, False, turn)
                        self.matrix[i][j] = ' '
                        best_score = score if score > best_score else best_score
        else:
            best_score = 99999
            for i in range(n):
                for j in range(n):
                    if self.matrix[i][j] == ' ':
                        self.matrix[i][j] = opponent
                        score = self.minimax(depth + 1, True, turn)
                        self.matrix[i][j] = ' '
                        best_score = score if score < best_score else best_score
        return best_score

    def menu(self):
        possible_args = ('user', 'easy', 'medium', 'hard')
        while True:
            command = input('Input command: ')
            args = command.split()
            if args[0].lower() == 'start' and args[1] in possible_args and args[2] in possible_args:
                self.play(args[1], args[2])  # no need to know the second arg
                break
            if args[0].lower() == 'exit':
                exit()
            else:
                print('Bad parameters!')

    def play(self, player1, player2):
        self.print_matrix()
        turn = 'X'
        player = player1
        while True:
            if player == 'user':
                x, y = self.input_coords()
                self.matrix[x][y] = turn
            elif player == 'easy':
                x, y = self.easy_coords()
                print('Making move level "easy"')
                self.matrix[x][y] = turn
            elif player == 'medium':
                x, y = self.medium_coords(turn)
                print('Making move level "medium"')
                self.matrix[x][y] = turn
            elif player == 'hard':
                x, y = self.hard_coords(turn)
                print('Making move level "hard"')
                self.matrix[x][y] = turn
            self.print_matrix()
            result = self.evaluate()
            if result is not None:
                if result == 'draw':
                    print('Draw')
                else:
                    print(f'{result} wins')
                break
            player = player2 if player == player1 else player1
            turn = 'O' if turn == 'X' else 'X'

    def print_matrix(self):
        print('-' * 9, sep='')
        for i in range(len(self.matrix)):
            print(f"| {' '.join(self.matrix[i])} |")
        print('-' * 9)

    def evaluate(self):
        for direction in (self.horizontal, self.vertical, self.primary_diagonal, self.secondary_diagonal, self.draw):
            result = direction()  # returns 'X' or 'O' or 'draw'
            if result:
                return result
        return None

    def draw(self):
        flat_matrix = [cell for cell in self.matrix for cell in cell]
        if ' ' not in flat_matrix:
            return 'draw'

    def horizontal(self):
        for row in self.matrix:
            set_row = set(row)
            if len(set_row) == 1 and ' ' not in set_row:
                return set_row.pop()

    def vertical(self):
        matrix_90 = [cell for cell in zip(*self.matrix)]
        for row in matrix_90:
            set_row = set(row)
            if len(set_row) == 1 and ' ' not in set_row:
                return set_row.pop()

    def primary_diagonal(self):
        diag1 = {self.matrix[i][i] for i in range(len(self.matrix))}
        if len(diag1) == 1 and ' ' not in diag1:
            return diag1.pop()

    def secondary_diagonal(self):
        n = len(self.matrix)
        diag2 = {self.matrix[i][j] for i in range(n) for j in range(n) if (i + j) == (n - 1)}
        if len(diag2) == 1 and ' ' not in diag2:
            return diag2.pop()


if __name__ == '__main__':
    tictactoe = TicTacToe()
    tictactoe.menu()
