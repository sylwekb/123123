import os
import redis
import requests

from datetime import datetime
from psycopg2.extras import Json
from .base import Base
from time import sleep

class NoFluffJobs(Base):

    BASE_URL = 'https://nofluffjobs.com/pl/job/'
    SEARCH_URL = 'https://nofluffjobs.com/api/search/posting'

    def get_proxy(self):
        redisConn = redis.Redis(host='redis', port=6379, db=0)
        while True:
            ip = redisConn.spop('working_ips')
            if ip is not None:
                ip = ip.decode('utf-8')
                proxy = {'http': ip, 'https': ip}
                return proxy
            else:
                sleep(1)


    def get_response(self, url):
        while True:
            try:
                response = requests.get(url, headers=self.HEADERS, proxies=self.get_proxy())
                return response
            except Exception as e:
                print(e)

    def get_jobs_from_api(self):
        data = self.get_response(self.SEARCH_URL)
        for offer in data.json().get('postings'):
            self.parse_and_insert_data(offer)
        self.conn.commit()
        self.conn.close()
        print("Commited queries - NoFluffJobs")


    def parse_and_insert_data(self, offer):
        title = offer.get('title')
        skills = Json([offer.get('technology')])
        category = offer.get('category')
        seniority = Json([lvl for lvl in offer.get('seniority')])
        url = self.BASE_URL + offer.get('url', '')
        salary_from = offer.get('salary',{}).get('from')
        salary_to = offer.get('salary',{}).get('to')
        salary_type = offer.get('salary',{}).get('type')
        salary_currency = offer.get('salary',{}).get('currency')
        online_interview = offer.get('onlineInterviewAvailable')
        company_name = offer.get('name')

        company_lat = None
        company_lon = None
        company_city = None
        company_street = None
        working_places = []
        for i in offer['location']['places']:
            company_city = i.get('city','')
            if company_city == 'Remote':
                working_places.append(company_city)
                company_street = None
            elif company_city is not None:
                company_lat = i.get('geoLocation',{}).get('latitude')
                company_lon = i.get('geoLocation',{}).get('longitude')
                street = i.get('street','')
                postalcode = i.get('postalCode')
                company_city = f'{company_city};{postalcode}'
                company_street = street
                working_places.append(company_city + company_street)

        article_added = offer.get('posted',None)
        article_renewed = offer.get('renewed',None)
        if isinstance(article_added, int):
            article_added = datetime.fromtimestamp(article_added / 1000)
        if isinstance(article_renewed, int):
            article_renewed = datetime.fromtimestamp(article_renewed / 1000)

        regions = offer.get('regions')
        if regions is not None:
            regions = Json(regions)

        self.c.execute("""INSERT INTO jobs (title, skills, category, seniority, url, 
            working_places, salary_from, salary_to, salary_type, salary_currency,
            online_interview, company_name, company_city, company_street, company_latitude, company_longtitude, 
            article_added, article_renewed, regions) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
            (title, skills, category, seniority, url, Json(working_places), salary_from, salary_to, salary_type, 
            salary_currency, online_interview, company_name, company_city,company_street, company_lat, company_lon,
            article_added, article_renewed, regions))