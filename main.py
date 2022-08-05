import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Create a URL object
streetsUrl = 'https://pe.usps.com/text/pub28/28apc_002.htm'

# Create object page
headers = {
    "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Mobile Safari/537.36'}
streetsPage = requests.get(streetsUrl, headers=headers)

# Obtain page's information
streetsSoup = BeautifulSoup(streetsPage.text, 'html.parser')

# Get the table by its id
streetsTable = streetsSoup.find('table', {'id': 'ep533076'})

# Transform the table into a list of dataframes
streetsDf = pd.read_html(str(streetsTable))

# Group together all "Commonly Used Street Suffix or Abbreviation" entries
streetsGroup = streetsDf[0].groupby(0)[1].apply(list)

for x in range(streetsGroup.size):

    dictionary = {
        "mappingType": "equivalent",
        "synonyms": streetsGroup[x]
    }

    # export the JSON into a file
    with open(streetsGroup.index.values[x] + ".json", "w") as outfile:
        json.dump(dictionary, outfile)


# Do the same for Secondary Unit Designators

# Create a URL object
unitsUrl = 'https://pe.usps.com/text/pub28/28apc_003.htm'

unitsPage = requests.get(unitsUrl, headers=headers)

# Obtain page's information
unitsSoup = BeautifulSoup(unitsPage.text, 'html.parser')

# Get the table by its id
unitsTable = unitsSoup.find('table', {'id': 'ep538257'})

# Transform the table into a list of dataframes
unitsDf = pd.read_html(str(unitsTable))

# Remove all blank values
unitsDf[0] = unitsDf[0].dropna()

# Create a 2D list that we will use for our synonyms
unitsList = unitsDf[0][[0, 2]].values.tolist()

# Remove all non-alphanumeric characters
unitsList = [[re.sub("[^ \w]"," ",x).strip().lower() for x in y] for y in unitsList]

# Restrict the range to only retrieve the results we want
for x in range(1, len(unitsList) - 1):

    dictionary = {
        "mappingType": "equivalent",
        "synonyms": unitsList[x]
    }

    # export the JSON into a file
    with open(unitsList[x][0] + ".json", "w") as outfile:
        json.dump(dictionary, outfile)
