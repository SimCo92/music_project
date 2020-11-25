from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_element_located, frame_to_be_available_and_switch_to_it, presence_of_all_elements_located, url_to_be
from selenium.webdriver.common.by import By

from datetime import date
import time
import os

from bs4 import BeautifulSoup
import requests

import pandas as pd

date = str(date.today())
i = 0
n_videos = 2500
loops = int(n_videos/100) + 1
sleep_time = 4
LINK = ''

# in case of error for chrome version check https://chromedriver.chromium.org/downloads

if os.name == 'nt':
    path = os.getcwd() + '/chromedriver_Win.exe'
else:
    path = os.getcwd() + '/chromedriver'

driverChrome = webdriver.Chrome(path)

with driverChrome as driver:

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-web-security')
    options.add_argument('--headless')
    options.add_argument('--allow-running-insecure-content')
    wait = WebDriverWait(driver, 50)
    
    # the link of the playlist
    wait.until(url_to_be(LINK))

    while i<loops:
            scroll = driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(sleep_time)
            i+=1

    result = driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
    df = pd.DataFrame(columns=['video_title', 'channel', 'link'])

    for i,r in enumerate(result):
        df.loc[i,'video_title'] = r.find_element_by_id('video-title').text
        df.loc[i,'channel'] = r.find_element_by_id('metadata').text
        df.loc[i,'link'] = r.find_element_by_css_selector('a').get_attribute('href')

    df.to_csv ('YT_liked_videos_' + date + '.csv', index = None, header=True)

    driver.close()

    df[['channel','video_title']].groupby('channel').count().sort_values(['video_title'], ascending = False).head(30)




