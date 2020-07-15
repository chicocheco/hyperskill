import os
import re
import sys
from collections import deque

import requests
from bs4 import BeautifulSoup
from colorama import Fore

name_folder = sys.argv[1]
if not os.path.exists(name_folder):
    os.mkdir(name_folder)

history = deque()
while True:
    url = input()

    if '.' in url:
        path = os.path.join(name_folder, '.'.join(url.split('.')[:-1]))
        r = requests.get(f'https://{url}')
        soup = BeautifulSoup(r.content, 'html.parser')
        n_scripts = len(soup.find_all('script'))
        for n in range(n_scripts):
            soup.script.decompose()  # remove from source
        for i in soup.find_all(text=True):
            if i.parent.name == 'a':
                print(f'{Fore.BLUE}{i}{Fore.RESET}')
            else:
                i = re.sub(r"(\|)+|(»)+", '', i).strip()
                if i:
                    print(i)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(soup.text)
    else:
        if url == 'exit':
            sys.exit()
        if url == 'back':
            history.pop()
            url = history.pop()
        try:
            path = os.path.join(name_folder, url)
            with open(path, 'r', encoding='utf-8') as file:
                print(file.read())
        except FileNotFoundError:
            print('error')
