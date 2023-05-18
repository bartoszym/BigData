import requests
from bs4 import BeautifulSoup


class OLXScraper:
    def __init__(self, url: str, pages_amount: int) -> None:
        self.url = url
        self.pages_amount = pages_amount

    def get_offers_list(self) -> list:
        to_ret = []
        for page_num in range(1, self.pages_amount + 1):
            print(f"Scraping {page_num} page...")
            self.url = self.url[:-1] + str(page_num)
            advertisements = self._get_advertisements()
            offers_list = []
            for advertisement in advertisements:
                offer_dict = self._scrap_advertisement(advertisement)
                offers_list.append(offer_dict)
            to_ret.extend(offers_list)

        return to_ret

    def _scrap_advertisement(self, advertisement) -> dict:
        offer_details = advertisement.find("div", {"class": "css-efx9z5"}).text
        production_year, mileage = offer_details.split("-")
        production_year = production_year.strip()
        mileage = mileage.replace("km", "").replace(" ", "").strip()
        price = advertisement.find("p", {"data-testid": "ad-price"}).text
        price = (
            price.replace("do negocjacji", "")
            .replace("zł", "")
            .replace(" ", "")
            .strip()
        )
        location = advertisement.find("p", {"data-testid": "location-date"}).text
        location = location.split("-")[0].strip()
        offer_dict = {
            "production_year": production_year,
            "mileage [km]": mileage,
            "price [zł]": price,
            "location": location,
        }
        return offer_dict

    def _get_advertisements(self) -> list:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content)
        advertisements = soup.find_all("div", {"class": "css-qfzx1y"})
        return advertisements
