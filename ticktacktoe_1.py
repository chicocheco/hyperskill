class TicTacToe:
    coordinates = {(1, 3): (0, 0), (2, 3): (0, 1), (3, 3): (0, 2),
                   (1, 2): (1, 0), (2, 2): (1, 1), (3, 2): (1, 2),
                   (1, 1): (2, 0), (2, 1): (2, 1), (3, 1): (2, 2)}

    def __init__(self, init_setup):
        self.init_setup = init_setup
        self.matrix = self.create_matrix()
        self.x, self.y = None, None

    def create_matrix(self):
        matrix = [[], [], []]
        for i, v in enumerate(self.init_setup):
            if v == '_':
                v = ' '
            if i < 3:
                matrix[0].append(v)
            elif 3 <= i < 6:
                matrix[1].append(v)
            else:
                matrix[2].append(v)
        return matrix

    def play(self):
        self.print_matrix()
        while True:
            try:
                a, b = (int(i) for i in input('Enter the coordinates: ').split())
                if not 0 < a < 4 or not 0 < b < 4:
                    print('Coordinates should be from 1 to 3!')
                    continue
                x, y = self.coordinates[a, b]
                if self.matrix[x][y] == 'X' or self.matrix[x][y] == 'O':
                    print('This cell is occupied! Choose another one!')
                    continue
                else:
                    self.matrix[x][y] = self.on_turn()
                    self.print_matrix()
                    if self.is_finished():
                        break
            except ValueError:
                print('You should enter numbers!')
                continue

    def on_turn(self):
        num_x = self.init_setup.count('X')
        num_o = self.init_setup.count('O')
        if num_x == num_o:
            return 'X'
        if num_x > num_o:
            return 'O'
        return 'E'

    def print_matrix(self):
        print('-' * 9, sep='')
        for i in range(len(self.matrix)):
            print(f"| {' '.join(self.matrix[i])} |")
        print('-' * 9)

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
        set_diag2 = {self.matrix[0][2], self.matrix[1][1], self.matrix[2][0]}
        if len(set_diag2) == 1 and ' ' not in set_diag2:
            print(f'{set_diag2.pop()} wins')  # upper-right to lower-left
            return True

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
        print('Game not finished')
        return True  # stage 1 requires this


if __name__ == '__main__':
    cells = input('Enter cells: ')
    # cells = '_XO_OX___'
    tictactoe = TicTacToe(cells)
    tictactoe.play()
