import os
import requests

from psycopg2.extras import Json
from .base import Base

class JustJoinIT(Base):

    BASE_URL = 'https://justjoin.it/offers/'
    SEARCH_URL = 'https://justjoin.it/api/offers'

    def get_jobs_from_api(self):
        data = requests.get(self.SEARCH_URL, headers=self.HEADERS)
        for offer in data.json():
            self.parse_and_insert_data(offer)
        self.conn.commit()
        self.conn.close()
        print("Commited queries - JustJoinIT")

    def parse_and_insert_data(self, offer):
        title = offer.get('title')

        skills = []
        skills_tmp = offer.get('skills')
        for skill in skills_tmp:
            skills.append(skill.get('name'))
        skills = Json(skills)

        seniority = Json(offer.get('experience_level'))
        url = self.BASE_URL + offer.get('id','')
        
        salary_from = offer.get('salary_from')
        salary_to = offer.get('salary_to')
        salary_type = offer.get('employment_type')
        salary_currency = offer.get('salary_currency','').upper()
        online_interview = offer.get('remote_interview')
        company_name = offer.get('name')
        company_city = offer.get('city')
        company_street = offer.get('street')
        company_lat = offer.get('latitude')
        company_lon = offer.get('longitude')
        article_added = offer.get('published_at')
        regions = Json(offer.get('country_code'))

        working_places = [] 
        if offer.get('remote') == True:
            working_places.append('Remote')
        if company_city is not None and company_adress is not None:
            working_places.append(f'{company_city};{company_adress}')
        working_places = Json(working_places)

        self.c.execute("""INSERT INTO jobs (title, skills,  seniority, url, 
            working_places, salary_from, salary_to, salary_type, salary_currency,
            online_interview, company_name, company_city, company_street, company_latitude, company_longtitude, 
            article_added, regions) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
            (title, skills, seniority, url, working_places, salary_from, salary_to, salary_type, salary_currency, 
            online_interview, company_name, company_city,company_street, company_lat, company_lon, article_added,
            regions))