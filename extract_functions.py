from selenium import webdriver
from bs4 import BeautifulSoup

from lxml import html
import math
import pandas as pd
import json

from functools import partial

# Instantiation of the path and the location of the chromedriver (Set this to the paths of your machine)
directory = "D:/Jupyter_Projects/Jupyter Notebooks/Textmining/Project"
chromedriver = "D:/Jupyter_Projects/Jupyter Notebooks/Textmining/Project/chromedriver.exe"

# I had set my configuration to false here, because I would not have been able to write to a file
headless = False

# Configuring the selenium webdriver
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : directory}
chromeOptions.add_experimental_option("prefs",prefs)
chromeOptions.add_argument("--disable-extensions")
if headless:
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--no-sandbox') # Headless can give errors, which are fixed with this but this also takes away the ability to write to a file somehow (only chrome has sandbox)
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

def get_titles_and_abstracts(url_and_count):
    url, count = url_and_count # Unpacking the url and the pagenumber
    driver.get(url) # Accessing pubmed with a given query containing the pagenumber

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extracting the titles and the abstracts using beautifulsoup
    titles = [str(title.text.replace('\n', '').strip()) for title in soup.findAll("h1", {"class": "heading-title"})]
    del titles[1::2] # Deletes every odd number index (because titles occur twice it appears)
    abstracts = [str(abstract.text.replace('\n', '').strip()) for abstract in soup.findAll("div", {"class": "abstract"})]
    
    # Writing the titles and the abstracts to their respective json file
    with open('saved_data/abstracts_{0}.json'.format(count), 'w') as json_file:
        json.dump({'titles': titles, 'abstracts': abstracts}, json_file)
       
    # Writing the pubmedIDS to their respective csv file
    with open('saved_data/pubmedIDs_{0}.csv'.format(count),'a') as csv_file:
        for strong in soup.findAll("strong", {"class": "current-id"}):
            csv_file.write(str(strong.text.replace('\n', '').strip()) + '\n')
        csv_file.close()
    
    # Quit the driver and close chrome
    driver.quit()