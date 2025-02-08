import urllib.request
from bs4 import BeautifulSoup
import re


def rePrinter(start, end, expression):
    _match = re.search(re.escape(start) + r'(.*?)' +
                       re.escape(end), expression)

    try:
        match_str = _match.group(1)
        cut1 = match_str
        cut2 = cut1[len(start):]
        cut = cut2[:-len(end)]
        print(cut)
    except:
        print("No match found")


url = "https://www.kleinanzeigen.de/s-fahrraeder/berlin/gold/k0c217l3331"

response = urllib.request.urlopen(url).read()

soup = BeautifulSoup(response, 'html.parser')

for script in soup(["script", "style"]):
    script.extract()

title = soup.title

print(title)

# save soup data to file

with open('bike_data.txt', 'w') as file:
    file.write(str(soup))
    file.close()


allthelisting = soup.find_all("article", {"class": "aditem"})

for listing in allthelisting:
    listing_string = str(listing)
    listing_string = listing_string.replace("\n", "")
    listing_string = listing_string.replace("><", ">\n<")
    print("NEW LISTING")
    # print(listing_string)
    name = listing.find("a", {"class": "ellipsis"})
    try:
        print(name.text)
    except:
        print("No name found")
    description = listing.find(
        "p", {"class": "aditem-main--middle--description"})

    print(description.text)
