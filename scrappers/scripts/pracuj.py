import requests
from bs4 import BeautifulSoup


class PracujPl(Base):

    BASE_URL = 'https://www.pracuj.pl/'
    START_URL = 'https://www.pracuj.pl/praca?rd=30&cc=5015%2c5016'

    def scrapp_jobs_from_page(self):
        r = requests.get(START_URL)
        soup = BeautifulSoup(r.text)
        import pdb; pdb.set_trace()

        while True:
            job_offers = soup.select('#results .offer__info , #results .offer--remoterecruitment , #results .offer-actions')
            for offer in job_offers:
                offer_soup = BeautifulSoup(offer)
                
                title = offer_soup.select_one('.offer-details__title-link')
                company_name = offer_soup.select_one('.offer-company__name')
                company_city = offer_soup.select_one('.offer-labels__item--location')
                article_added = offer_soup.select_one('.offer-actions__date').get_text()
                features = offer_soup.select('.offer-labels--hide-on-mobile .offer-labels__item')
                href = title.get('href')
                if href is None:
                    job_offers_ = offer_soup.select('.offer-regions__label').get('href')
                    for offer_ in job_offers_:
                        self.parse_and_insert_data(offer_)
                else:
                    self.parse_and_insert_data(href)

            next_page = soup.select_one('.pagination_element--next .pagination_trigger').get('href')
            if next_page is None:
                break

            r = requests.get(START_URL)
            soup = BeautifulSoup(r.text)
    
    def parse_and_insert_data(self, url, title, ):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        import pdb; pdb.set_trace()

        title = soup.select_one('.OfferView1Z5qAH')
        skills = soup.
        category = soup.

        if 'junior' in title.lower(): seniority = 'Junior'
        elif 'mid' or 'regular' in title.lower(): seniority = 'Mid'
        elif 'senior' in title.lower(): seniority = 'Senior'
        else: seniority = None

        url = url
        working_places = soup.
        salary_from = soup.
        salary_to = soup.
        salary_type = soup.
        salary_currency = soup.
        online_interview = soup.select_one('.OfferView1WH6YK')
        company_name = soup.select_one('.OfferViewFf0I7D')
        company_city = soup.
        company_street = soup.
        company_lat = soup.
        company_lon = soup.
        article_added = soup.
        article_renewed = soup.
        regions = soup.


        
        



