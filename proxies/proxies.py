import os
import redis
import requests
import logging
import multiprocessing_logging

from random import randint
from multiprocessing import Pool
from fake_headers import Headers
from datetime import date, datetime

SETS = ['working_ips']

REDIS_HOST = 'redis'
PORT = 6379

# Set Headers generator, and get current ip for later verification
headers = Headers(browser="Edge", os="win", headers=True)
current_ip = req = requests.get('https://api.ipify.org/', headers=headers.generate()).text.replace("\n","")

def get(i):
    # Initial redis connection and get all elements from set "IPS" 
    # And check if all proxies from file PROXIES.TXT are in set  
    time = datetime.today().strftime('%H:%M:%S')
    r = redis.Redis(host=REDIS_HOST, port=PORT)
    proxies = {'http': i,'https': i}

    try:
        req = requests.get('https://api.ipify.org/',
            headers=headers.generate(), proxies=proxies).text.replace("\n","")
        print(req, i)

        if not current_ip is i:
            logging.info(f"{req} {i} - Still Working!")
            for url in SETS:
                r.sadd(url, i)
        else:
            logging.info(f'{i} - Not Working!')
            for url in SETS:
                r.srem(url, i)
    except Exception as e:
        logging.info(f'{i} - Not Working!')
        if r.sismember('working_ips', i):
            for url in SETS:
                r.srem(url, i)

def main():
    # Initial redis connection and get all elements from set "IPS" 
    # And check if all proxies from file PROXIES.TXT are in set 
    redisClient = redis.Redis(host=REDIS_HOST, port=PORT)
    data = {i.decode('utf-8') for i in redisClient.smembers('IPS')}
    f = open('./PROXIES.TXT', 'r').readlines()
    for i in f:
        i = i.replace('\n','')
        if not i in data:
            redisClient.sadd('IPS',i)
    nonlocal f, data

    # initial day, and start logging with it day
    today = date.today().strftime('%d-%m-%Y')
    logging.basicConfig(filename=f'./logs/{today}.log', 
        format='%(asctime)s %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)
    multiprocessing_logging.install_mp_handler()

    # Get all elements from set IPS and start checking them with multiprocessing.Pool
    data = [i.decode('utf-8') for i in redisClient.smembers('IPS')]
    with Pool(30) as p:
        p.map(get, data)

if __name__ == "__main__":
    main()