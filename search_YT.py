from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_element_located

# import requests
import datetime
import time
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

date = str(datetime.date.today())
path = os.getcwd() + '/chromedriver'

playlist_df = pd.read_csv("UANMUSIC.csv")



playlist_df['link'] = "https://www.youtube.com/results?search_query=" + \
                        playlist_df['artist'].replace(' ', '+') + \
                        '+' + \
                        playlist_df['song'].replace(' ', '+')

link_watch = []
# with webdriver.Chrome(path) as driver:
with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 5)
    for link in playlist_df['link']:
        driver.get(link)
        contents = wait.until(presence_of_element_located((By.ID, "contents")))
        page_html = contents.get_attribute('innerHTML')
        soap = BeautifulSoup(page_html, 'html.parser')
        link = soap.find("a", {'id':'thumbnail'})['href']
        link_watch.append(link)
        print(link)
        
playlist_df['link_watch'] = ["https://www.youtube.com" + x for x in link_watch]

playlist_df.to_csv("UANMUSIC_link.csv")


## passando dalla barra di search

# # with webdriver.Chrome(path) as driver:
# with webdriver.Firefox() as driver:
#     wait = WebDriverWait(driver, 5)
#     driver.get(LINK)
#     wait.until(presence_of_element_located((By.ID, "search-form")))
#     wait.until(presence_of_element_located((By.CSS_SELECTOR, "input"))).send_keys("ciao")

