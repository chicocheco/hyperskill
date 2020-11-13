from collections import deque
from sys import exit


class Calculator:

    def __init__(self):
        self.split_inp = None
        self.digits = None
        self.ops = None
        self.vars = {}
        self.run()

    def get_vars(self, inp):
        try:
            k, v = (i.strip() for i in inp.split('='))
        except ValueError:
            print('Invalid identifier')
        else:
            if not k.isalpha():
                print('Invalid identifier')
                return
            if v in self.vars:
                self.vars[k] = self.vars[v]
            elif not v.isdigit():
                print('Invalid identifier')
                return
            else:
                self.vars.update([(k, v)])
            return

    def run(self):
        while True:
            inp = input()
            if not inp:
                continue
            if inp.startswith('/'):
                self.check_command(inp)
                continue
            if '=' in inp:  # adding variables
                self.get_vars(inp)
                continue
            self.split_inp = inp.split()
            if len(self.split_inp) == 1 and self.split_inp[0] not in self.vars:
                print('Unknown variable')

            self.assign_values()
            self.get_digits()
            if len(self.digits) == 1:
                print(self.digits[0])
                continue
            self.get_operators()
            self.compute()

    def get_operators(self):
        raw_ops = [op for op in self.split_inp if not op[-1].isdigit() and '-' in op or '+' in op]
        self.ops = deque(['+' if len(op) % 2 == 0 and '+' not in op else op[0] for op in raw_ops])  # -- becomes +

    def get_digits(self):
        self.digits = deque([int(n) for n in self.split_inp if n.lstrip('-+').isdigit()])

    def assign_values(self):
        if self.vars:
            for key in self.split_inp:
                if key in self.vars:
                    i = self.split_inp.index(key)
                    self.split_inp[i] = self.vars[key]

    @staticmethod
    def check_command(inp):
        if inp == '/exit':
            print('Bye!')
            exit()
        if inp == '/help':
            print('The calculator supports addition and subtraction where -- equals +')
        else:
            print('Unknown command')

    def compute(self):
        last_num = None
        while self.digits and self.ops:
            if last_num is None:
                last_num = self.digits.popleft()
            operation = self.ops.popleft()
            second = self.digits.popleft()
            if operation == '+':
                last_num += second
            elif operation == '-':
                last_num -= second
        if last_num is not None:
            print(last_num)
        else:
            print('Invalid expression')


if __name__ == '__main__':
    Calculator()
