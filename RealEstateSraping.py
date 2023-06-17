import requests
from bs4 import BeautifulSoup

#define scraping function
def scrape_real_estate_data(city):
    #format city name into a url
    city_url = city.replace(' ', '-')
    #Request a HTTP from realestate website
    url = f"(https://www.zillow.com/in-{city_url}/list-1"
    response = requests.get(url)
    #check if the request was successful
    if response.status_code == 200:
        #parse the response
        soup = BeautifulSoup(response.content, 'html.parser')   
        #find listing
        listings = soup.find_all('div', class_='listing')
        #Catalog dictionary to store data
        catalog = {}
        #iterate through listings
        for listing in listings:
            title = listing.find("h2").text
            listing_type = listing.find("span", class_="type").text
            #add to catalog
            if listing_type in catalog:
                catalog[listing_type].append(title)
            else:
                catalog[listing_type] = [title]
        return catalog
    #if request was unsuccessful
    else:
        print("Request failed")
        return None
city = input("Enter a city: ")

#call the function

data = scrape_real_estate_data(city)

#print the data
if data:
    print(f"Real estate data for {city}")
    for listing_type, listings in data.items():
        print(f"{listing_type}: {len(listings)}")
        for listing in listings:
            print(f" - {listing}")
# if not data:
else:
    print("No data found")
    
            
