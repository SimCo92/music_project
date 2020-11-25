from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_element_located, frame_to_be_available_and_switch_to_it, presence_of_all_elements_located

import time
import os
from bs4 import BeautifulSoup
import pandas as pd

LINK = 'https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dit%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F%253Fgl%253DCO&hl=it&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
mail = 's.colonna92@gmail.com'
pw = 'Venoms92'
pathchrome = os.getcwd() + '/chromedriver'
path = os.getcwd()

# '--disable-web-security', '--user-data-dir', '--allow-running-insecure-content' 

with webdriver.Chrome(pathchrome) as driver:

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-web-security')
    options.add_argument('--user-data-dir')
    options.add_argument('--allow-running-insecure-content')

    wait = WebDriverWait(driver, 20)
    
    driver.get(LINK)
    # time.sleep(100)



    
    wait.until(presence_of_element_located((By.ID, "identifierId"))).send_keys(mail)
    wait.until(element_to_be_clickable((By.ID, "identifierNext"))).click()
    time.sleep(20)
    # wait.until(presence_of_element_located((By.ID, "txtUsername"))).send_keys(mail)
    # wait.until(presence_of_element_located((By.ID, 'txtRealPassword'))).click()
    # # .send_keys(pw)
    # time.sleep(5)

    # return driver