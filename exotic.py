import time
import os
import gc

import requests
from pyuseragents import random as random_useragent
import threading
from loguru import logger


logger.add("logs.log", level="INFO", mode="a", encoding="utf-8")


mail_file = str(input("input ur file with mails: ")) 
with_proxy = str(input("with proxy? (y/n): "))

if with_proxy == "y":
    proxy = str(input("Input mobile proxy (login:pass@ip:port:url:key): ")).split(":")

else:
    thread_count = int(input("input threads count: "))

with open(mail_file, encoding="utf-8") as f:
    mails =  f.readlines()

def main():
    for mail in mails:
        try:
            mails.pop(mails.index(mail))
            mail = mail.split(":")[0]

            # change proxy
            if with_proxy == "y":
                r = requests.get(
                    url = "https:" + proxy[-2],
                    headers={"User-Agent": random_useragent()},
                    params={
                        "proxy_key":proxy[-1],
                        "format": "json"
                    })

                if r.json()["status"] == "OK":
                    logger.info("ip was changed succesfully")

                else:
                    logger.warning("proxy err")
                    continue

            headers = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6", "content-type": "application/json; charset=UTF-8", "origin": "https://exotic.markets", "referer": "https://exotic.markets/", "user-agent": random_useragent(), "x-remoting-proxy": "true"}
            url = "https://exotic.markets/api/RegisterEmail"

            if with_proxy == "y":
                rqmail = requests.post(
                    url=url, 
                    headers=headers,
                    json=[{"Email": mail}],
                    proxies={
                        "http": f"http://{':'.join([str(_) for _ in proxy[0:3]])}",
                        "https": f"http://{':'.join([str(_) for _ in proxy[0:3]])}"
                        })                   
            else:
                rqmail = requests.post(url=url, headers=headers, json=[{"Email": mail}])


            if rqmail.status_code == 200:
                logger.success(f"{mail} - OK")


        except Exception as error: 
            logger.error(error)
            continue
    

def clear():
    while True:
        os.system('cls')
        gc.collect()
        time.sleep(30)

if __name__ == '__main__':

    os.system('cls')
    threading.Thread(target=clear).start() 
    if with_proxy == "y":
        threading.Thread(target=main).start()    
    else:
        for _ in range(thread_count):
            threading.Thread(target=main).start()
