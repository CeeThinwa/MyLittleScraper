import requests
from bs4 import BeautifulSoup
import html5lib
import pandas as pd
import numpy as np
from IPython.display import HTML
import base64

# PHASE 1: EXTRACTION OF LINKS
# My data is the first 25 pages of a search query for "Marketing research" on Indeed:
urls = ['https://www.indeed.com/jobs?q=Marketing+research&l=',
        'https://www.indeed.com/jobs?q=Marketing+research&start=10',
        'https://www.indeed.com/jobs?q=Marketing+research&start=20',
        'https://www.indeed.com/jobs?q=Marketing+research&start=30',
        'https://www.indeed.com/jobs?q=Marketing+research&start=40',
        'https://www.indeed.com/jobs?q=Marketing+research&start=50',
        'https://www.indeed.com/jobs?q=Marketing+research&start=60',
        'https://www.indeed.com/jobs?q=Marketing+research&start=70',
        'https://www.indeed.com/jobs?q=Marketing+research&start=80',
        'https://www.indeed.com/jobs?q=Marketing+research&start=90',
        'https://www.indeed.com/jobs?q=Marketing+research&start=100',
        'https://www.indeed.com/jobs?q=Marketing+research&start=110',
        'https://www.indeed.com/jobs?q=Marketing+research&start=120',
        'https://www.indeed.com/jobs?q=Marketing+research&start=130',
        'https://www.indeed.com/jobs?q=Marketing+research&start=140',
        'https://www.indeed.com/jobs?q=Marketing+research&start=150',
        'https://www.indeed.com/jobs?q=Marketing+research&start=160',
        'https://www.indeed.com/jobs?q=Marketing+research&start=170',
        'https://www.indeed.com/jobs?q=Marketing+research&start=180',
        'https://www.indeed.com/jobs?q=Marketing+research&start=190',
        'https://www.indeed.com/jobs?q=Marketing+research&start=200',
        'https://www.indeed.com/jobs?q=Marketing+research&start=210',
        'https://www.indeed.com/jobs?q=Marketing+research&start=220',
        'https://www.indeed.com/jobs?q=Marketing+research&start=230',
        'https://www.indeed.com/jobs?q=Marketing+research&start=240']

# First load the raw data into an array
data = []

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    info_block = soup.find_all("div", attrs={"class":"title"})
    data.append(info_block)

# Then make that array a dataframe,
data_df = pd.DataFrame(data)

# label the row index
data_df.index.name = 'Page Number'

# and rename the rows and columns
pages = ['page_1', 'page_2', 'page_3', 'page_4', 'page_5',
         'page_6', 'page_7', 'page_8', 'page_9', 'page_10',
         'page_11', 'page_12', 'page_13', 'page_14', 'page_15',
         'page_16', 'page_17', 'page_18', 'page_19', 'page_20',
         'page_21', 'page_22', 'page_23', 'page_24', 'page_25']

results = ['result_1', 'result_2', 'result_3', 'result_4', 'result_5',
           'result_6', 'result_7', 'result_8', 'result_9', 'result_10']

data_df.index = pages
data_df.columns = results

# Make everything in the dataframe a string
data_df = data_df.astype('str')

# And strip each string down to get the link
strings = []

for result in results:
    a = data_df[result].str.split()
    i = 0

    for page in pages:
        b = a.loc[page]
        href = b[6]
        strings.append(href)

strings_s = pd.Series(strings)
strings_s = strings_s.str.replace('href="/rc/clk', 'https://www.indeed.com/viewjob')
strings_s = strings_s.str.replace('"', '')

# PHASE 2 : CONTENT HARVESTING & LOCAL DATA STORAGE
# Get content inside each link
new_urls = strings_s.values.tolist()

new_data = []

i = 0
for i in range(0,len(new_urls)):
    new_r = requests.get(new_urls[i])
    new_urls[i] = new_r.url
    new_soup = BeautifulSoup(new_r.content, "html5lib")
    new_info_block = new_soup.find_all("div", attrs={"class":"jobsearch-jobDescriptionText"})
    new_data.append(new_info_block)

# Save mined data and add timestamp
from datetime import datetime

new_data_df = pd.DataFrame(new_data)
new_data_df = new_data_df.astype('str')

filename = datetime.now().strftime('search_data_mined-%d-%m-%Y-%H-%M.csv')
new_data_df.to_csv('C://Users//CT//Downloads//'+filename)









