from bs4 import BeautifulSoup
import requests

url = "https://www.newegg.ca/gigabyte-geforce-rtx-3050-gv-n3050eagle-8gd/p/N82E16814932497?Item=N82E16814932497"
result = requests.get(url)

doc = BeautifulSoup(result.text, 'html.parser')

print(doc.prettify())

prices = doc.find_all(text = "$")

print(prices)
parent = prices[0].parent

print(parent)

strong = parent.find("strong")

print(strong.string)