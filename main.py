import requests
import re
from time import time
from bs4 import BeautifulSoup

website = 'https://www.kijiji.ca'
url = 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/c37l1700281?ad=offering'
numberOfRentals = 0
total = 0

while(True):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    items = [item.getText().strip() for item in soup.find_all("div", {"class", "price"})]
    prices = [int(re.sub("[^0-9]", "", item)) / 100 for item in items if item != "Sur demande" and item != "Échange"]
    fair_prices = [price for price in prices if 5000 > price > 0]
    total += sum(fair_prices)
    numberOfRentals += len(fair_prices)
    print(numberOfRentals)
    try:
        url = website + soup.find(title="Suivante").get('href')
    except:
        break

avgListingPrice = total / numberOfRentals
print(avgListingPrice)


