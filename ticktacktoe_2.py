from random import randint


class TicTacToe:
    coordinates = {(1, 3): (0, 0), (2, 3): (0, 1), (3, 3): (0, 2),
                   (1, 2): (1, 0), (2, 2): (1, 1), (3, 2): (1, 2),
                   (1, 1): (2, 0), (2, 1): (2, 1), (3, 1): (2, 2)}

    def __init__(self):
        self.matrix = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.occupied_coords = set()

    def get_coords(self):
        while True:
            a, b = (int(i) for i in input('Enter the coordinates: ').split())
            if not 0 < a < 4 or not 0 < b < 4:
                print('Coordinates should be from 1 to 3!')
            else:
                x, y = self.coordinates[a, b]
                break
        return x, y

    def create_random_coords(self):
        while True:
            x_rand, y_rand = (randint(0, 2) for _ in range(2))
            if (x_rand, y_rand) not in self.occupied_coords:
                return x_rand, y_rand

    def is_free(self, x, y):
        if (x, y) in self.occupied_coords:
            print('This cell is occupied! Choose another one!')
            return False
        self.occupied_coords.add((x, y))
        return True

    def play(self):
        self.print_matrix()
        human = True
        while True:
            try:
                x, y = self.get_coords() if human else self.create_random_coords()
                if self.is_free(x, y):
                    if human:
                        self.matrix[x][y] = 'X'
                        human = False
                    else:
                        self.matrix[x][y] = 'O'
                        print('Making move level "easy"')
                        human = True
                    self.print_matrix()
                if self.is_finished():
                    break
            except ValueError:
                print('You should enter numbers!')
                continue

    def print_matrix(self):
        print('-' * 9, sep='')
        for i in range(len(self.matrix)):
            print(f"| {' '.join(self.matrix[i])} |")
        print('-' * 9)

    def is_finished(self):
        flat_matrix = [cell for cell in self.matrix for cell in cell]
        if any([self.horizontal_dir(),
                self.vertical_dir(),
                self.diagonal_dir_a(),
                self.diagonal_dir_b()]):
            return True
        if ' ' not in flat_matrix:
            print('Draw')
            return True

    def horizontal_dir(self):
        for row in self.matrix:
            set_row = set(row)
            if len(set_row) == 1 and ' ' not in set_row:
                print(f'{set_row.pop()} wins')  # horizontally
                return True

    def vertical_dir(self):
        grid_90 = [cell for cell in zip(*self.matrix)]
        for row in grid_90:
            set_row = set(row)
            if len(set_row) == 1 and ' ' not in set_row:
                print(f'{set_row.pop()} wins')  # vertically
                return True

    def diagonal_dir_a(self):
        diag1 = []
        for i in range(len(self.matrix)):
            diag1.append(self.matrix[i][i])
        set_diag1 = set(diag1)
        if len(set_diag1) == 1 and ' ' not in set_diag1:
            print(f'{set_diag1.pop()} wins')  # upper-left to lower-right
            return True

    def diagonal_dir_b(self):
        # TODO: hardcoded coordinates
        set_diag2 = {self.matrix[0][2], self.matrix[1][1], self.matrix[2][0]}
        if len(set_diag2) == 1 and ' ' not in set_diag2:
            print(f'{set_diag2.pop()} wins')  # upper-right to lower-left
            return True


if __name__ == '__main__':
    tictactoe = TicTacToe()
    tictactoe.play()
