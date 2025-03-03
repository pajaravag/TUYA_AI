import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, headers):
        self.headers = headers

    def scrape_credit_cards(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            card_elements = soup.find_all("h2")
            credit_cards = [element.get_text(strip=True) for element in card_elements if "Tarjeta" in element.get_text(strip=True) and \
                            "crédito" not in element.get_text(strip = True).lower()]
            return sorted(set(credit_cards))
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []

    def scrape_credicompras(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            interest_rates = [section.get_text(strip=True) for section in soup.find_all("p") if "Tasa Efectiva Anual" in section.get_text(strip=True)]
            policy_details = [section.get_text(strip=True) for section in soup.find_all("p") if "Póliza colectiva" in section.get_text(strip=True) or "seguro deudores" in section.get_text(strip=True)]
            structured_data = {
                "Credicompras": {
                    "Interest Rates": list(set(interest_rates)),
                    "Insurance Policy": list(set(policy_details))
                }
            }
            return structured_data
        else:
            print(f"❌ Failed to retrieve the page. Status code: {response.status_code}")
            return {}