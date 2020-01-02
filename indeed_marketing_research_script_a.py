import requests
from bs4 import BeautifulSoup
import html5lib
import pandas as pd
import numpy as np
from IPython.display import HTML
import base64

# PHASE 1: EXTRACTION OF LINKS
# My data is the first 25 pages of a search query for "Marketing research" on Indeed:

# First load the raw data into an array
data = []

#then scrape data from search result pages
pgs = ['l=', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
      11 ,12, 13, 14, 15, 16, 17, 18, 19, 20,
      21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
      31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
      41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
      51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
      61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
      71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
      81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
      91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

for pg in pgs:
    if pg != 'l=':
       r = requests.get('https://www.indeed.com/jobs?q=Marketing+research&start='+str(pg)+'0')
    else:
        r = requests.get('https://www.indeed.com/jobs?q=Marketing+research&'+str(pg))     
    
    soup = BeautifulSoup(r.content, "html5lib")
    info_block = soup.find_all("a", attrs={"class":"jobtitle turnstileLink"})
    test_info_block = str(info_block)
    new = test_info_block.split(' href="', 10)

    i=1
    for i in range(11):
        new_new = new[i].split('" id=', 1)
        link = new_new[0].replace('/rc/clk', 'https://www.indeed.com/viewjob')
        data.append(link)

# Turn into a dataframe
data_df = pd.DataFrame(data)
data_df.columns = ['links']

# and filter out values that are not links
data_df = data_df[~data_df.links.str.startswith('[<a class')]



# PHASE 2 : CONTENT HARVESTING
# Get content inside each link
new_data = []

i=0
for i in range(250):
    new_r = requests.get(data_df.links.iloc[i])
    new_soup = BeautifulSoup(new_r.content, "html5lib")
    new_info_block = new_soup.find_all("div", attrs={"class":"jobsearch-jobDescriptionText"})
    new_data.append(new_info_block)

# Save mined data and add timestamp
new_data_df = pd.DataFrame(new_data)
new_data_df = new_data_df.astype('str')

filename = datetime.now().strftime('search_data_mined-%d-%m-%Y-%H-%M.csv')
new_data_df.to_csv('C://Users//adrian//Downloads//'+filename)










