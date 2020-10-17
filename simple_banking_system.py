from random import randint
from sys import exit
import sqlite3


class BankingSystem:
    menu = "1. Create an account\n" \
           "2. Log into account\n" \
           "0. Exit\n"
    menu_li = "1. Balance\n" \
              "2. Add income\n" \
              "3. Do transfer\n" \
              "4. Close account\n" \
              "5. Log out\n" \
              "0. Exit\n"

    def __init__(self):
        self.conn, self.cur = self.connect_db()
        self.logged_in = False
        self.curr_card_num = None
        self.balance = None

    def run(self):
        while True:
            if self.logged_in:
                self.user_menu()
            else:
                self.start_menu()

    @staticmethod
    def connect_db():
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
        );""")
        conn.commit()
        return conn, cur

    def terminate(self):
        self.cur.close()
        self.conn.close()
        print('Bye!')
        exit()

    def start_menu(self):
        inp = input(self.menu)
        if inp == '1':
            card_n = self.create_card_num()
            pin = str(randint(0000, 9999)).zfill(4)
            print(f'Your card number:\n{card_n}')
            print(f'Your card PIN:\n{pin}')
            self.cur.execute('INSERT INTO card (pin, number) VALUES (?, ?)', (pin, card_n))
            self.conn.commit()
        elif inp == '2':
            in_card = input('Enter your card number:\n')
            in_pin = input('Enter your PIN:\n')
            self.cur.execute('SELECT balance FROM card WHERE pin = ? AND number = ?', (in_pin, in_card))
            found_row = self.cur.fetchone()
            if found_row is not None:
                print('You have successfully logged in!')
                self.curr_card_num = in_card
                self.balance = found_row[0]
                self.logged_in = True  # TODO: could be discarded?
            else:
                print('Wrong card number or PIN!')
        elif inp == '0':
            print('Bye!')
            self.terminate()

    def user_menu(self):
        options_li = {'1': self.print_balance,
                      '2': self.add_income,
                      '3': self.do_transfer,
                      '4': self.close_acc,
                      '5': self.log_out,
                      '0': self.terminate
                      }
        options_li.get(input(self.menu_li))()  # call func with () operator

    def print_balance(self):
        print(f'Balance: {self.balance}')

    def add_income(self):
        amount = int(input('Enter income:\n'))
        self.balance += amount
        self.cur.execute('UPDATE card SET balance = ? WHERE number = ?', (self.balance, self.curr_card_num))
        self.conn.commit()
        print('Income was added!')

    def do_transfer(self):
        inp_other_card_n = input('Transfer\nEnter card number:\n')
        cn_no_check = inp_other_card_n[:-1]
        checksum_luhn = self.calc_checksum(cn_no_check)
        if checksum_luhn != inp_other_card_n[-1]:
            print('Probably you made a mistake in the card number. Please try again!')
        else:
            self.cur.execute('SELECT balance FROM card WHERE number = ?', (inp_other_card_n,))
            found_row = self.cur.fetchone()
            if found_row is not None:
                other_balance = found_row[0]
                inp_add_amount = int(input('Enter how much money you want to transfer:\n'))
                if inp_add_amount > int(self.balance):
                    print('Not enough money!')
                else:
                    new_other_balance = other_balance + inp_add_amount
                    self.cur.execute('UPDATE card SET balance = ? WHERE number = ?',
                                     (new_other_balance, inp_other_card_n))
                    self.conn.commit()
                    # calc the rest of money on user's acc and update in db
                    self.balance = str(int(self.balance) - inp_add_amount)
                    self.cur.execute('UPDATE card SET balance = ? WHERE number = ?',
                                     (self.balance, self.curr_card_num))
                    self.conn.commit()
                    print('Success!')
            else:
                print('Such a card does not exist.')

    def close_acc(self):
        self.cur.execute('DELETE FROM card WHERE number = ?', (self.curr_card_num,))
        self.conn.commit()
        print('The account has been closed!')

    def log_out(self):
        print('You have successfully logged out!')
        self.logged_in = False

    def create_card_num(self):
        iin = '400000'
        gen_number = str(randint(000000000, 999999999)).zfill(9)  # for leading zeros
        cn_no_check = iin + gen_number
        checksum_luhn = self.calc_checksum(cn_no_check)
        card_n = cn_no_check + checksum_luhn
        return card_n

    @staticmethod
    def calc_checksum(cn_no_check):
        # double odd digits
        ctrl_n_odd_doubled = [int(n) * 2 if i % 2 == 0 else int(n) for i, n in enumerate(cn_no_check)]
        # subtract 9 to digits over 9
        ctrl_n_sub = [i - 9 if i > 9 else i for i in ctrl_n_odd_doubled]
        ctrl_n_sum = sum(ctrl_n_sub)
        # if it's a multiple of 10, return 0, otherwise make it
        checksum_luhn = str(0 if ctrl_n_sum % 10 == 0 else abs((ctrl_n_sum % 10) - 10))
        return checksum_luhn


if __name__ == '__main__':
    atm = BankingSystem()
    atm.run()
