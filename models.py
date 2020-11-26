# funzionante
# bisogna creare package e migliorare performance

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import time
import os

from bs4 import BeautifulSoup
import requests
import pandas as pd



def get_playlist(driver,link,n_videos,sleep_time):

    driver.get(link)
    playlistname = driver.title

    i = 0
    loops = int(n_videos/100) +1
    while i<loops:
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(sleep_time)
        i+=1

    result = driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
    songs = pd.DataFrame(columns=['name', 'metadata', 'link_yt'])

    for song in result:
        name = song.find_element_by_id('video-title').text
        metadata = song.find_element_by_id('metadata').text
        link = song.find_element_by_css_selector('a').get_attribute('href')
        songs = songs.append([{'name':name, 'metadata':metadata, 'link_yt' :link}])

    return playlistname, songs

    # songs.to_csv( playlistname + ' - ' + date +'.csv')