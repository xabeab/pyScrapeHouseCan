"""
NOT MEANT FOR PRODUCTION

I'm just trying to figure out how to access the pertinent elements from the parsed html (beautifulsoup object)
"""
import Ad

# Test url, I just selected a random ad
url = "https://www.kijiji.ca/v-appartement-condo/ville-de-montreal/soyez-au-coeur-des-evenements-montrealais-super-studio-luxueux/1550238430"

ad = Ad.Ad(url)

ad.print_attributes()

ad.parse_with_soup()

print(ad.soup())

soup = ad.soup

# get body
mainContainer = soup.body.find_all("div")[1]

# get main page content
mainPageContent = mainContainer.find_all("div")[1]

# get viewItemPage
viewItemPage = mainPageContent.find_all("div")



