from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_element_located
from pytube import YouTube
import pandas as pd
import discogs_client
import time
import requests
import json


def get_playlist_YT(driver,link):

    """ get a diver and a YT playlist link and
    return playlistname, pandas dataframe columns=['name', 'metadata', 'link_yt']"""

    driver.get(link)
    playlistname = driver.title
    result = driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
    songs = pd.DataFrame(columns=['name', 'metadata', 'link_yt'])
    for song in result:
        name = song.find_element_by_id('video-title').text
        metadata = song.find_element_by_id('metadata').text
        link = song.find_element_by_css_selector('a').get_attribute('href')
        songs = songs.append([{'name':name, 'metadata':metadata, 'link_yt' :link}])
    return playlistname, songs



def search_YT(driver,df):

    """ Receive driver and a df['artist','song'] and
        return a dataframe['artist','song','link_search', 'link_watch']"""

    playlist_df = df
    playlist_df['link_search'] = "https://www.youtube.com/results?search_query=" + \
                        playlist_df['artist'].replace(' ', '+') + \
                        '+' + \
                        playlist_df['song'].replace(' ', '+')

    wait = WebDriverWait(driver, 5)
    for link in playlist_df['link_search']:
        driver.get(link)
        contents = wait.until(presence_of_element_located((By.ID, "contents")))
        page_html = contents.get_attribute('innerHTML')
        soap = BeautifulSoup(page_html, 'html.parser')
        link = soap.find("a", {'id':'thumbnail'})['href']
        link_watch.append(link)
        print(link)

    playlist_df['link_watch'] = ["https://www.youtube.com" + x for x in link_watch]
    return playlist_df




def YT_likedvideos(driver, link, n_videos = 10, SCROLL_PAUSE_TIME = 5, sleep_time = 3):
    """ get driver, link of a yt liked videos, n_videos = 10, SCROLL_PAUSE_TIME = 5, sleep_time = 3 and return
        a dataframe columns=['video_title', 'channel', 'link']"""

    driver.get(link)
    i = 0
    loops = int(n_videos/100) +1

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

    return df




def downloadlist(video_link):

    for v in video_link:
        print(v)
        try:
            yt = YouTube(v)
            audio = yt.streams.filter(only_audio=True).first()
        except:
            print('exception')
            time.sleep(10)
            yt = YouTube(v)
            audio = yt.streams.filter(only_audio=True).first()
        if command_output:
            audio.download(command_output)
        else:
            audio.download()




def add_discogs_metadata(video_title_list,token_key):

    """ get a video_title_list and a token_key from DiscogsAPI and return a 
        pandas df columns=['video_title','styles','label','year','country','community']"""

    df_result = pd.DataFrame(columns=['styles','label','year','country','community'])
    search_n = len(video_title_list)
    print("\n----------------------\n Search to process: ", search_n, "\n----------------------\n")

    for i,title in enumerate(video_title_list):

        print(i, " - Still ", search_n - i , " to process")
        title_search = str(title).replace(' ', '+').replace("'","%27")
        link = "https://api.discogs.com/database/search?q=" + title_search + "&key=" + token_key
        print(link)
        response = requests.get(link)._content.decode('utf-8') # Decode using the utf-8 encoding
        response_json = json.loads(response)
        
        if 'message' in response_json.keys():
            time.sleep(60)
            response = requests.get(link)._content.decode('utf-8') # Decode using the utf-8 encoding
            response_json = json.loads(response)
        
        df_result.loc[i,'video_title'] = title
        
        if str('results') in response_json.keys():
            if len(response_json['results']) > 0:
                if str('title') in response_json['results'][0].keys():
                    df_result.loc[i,'video_titleDGS'] = response_json['results'][0]['title']
                    print('video_titleDGS: ', df_result.loc[i,'video_titleDGS'])
                if str('style') in response_json['results'][0].keys():
                    df_result.loc[i,'styles'] = response_json['results'][0]['style']
                    print('styles: ', df_result.loc[i,'styles'])
                if str('label') in response_json['results'][0].keys():
                    df_result.loc[i,'label'] = response_json['results'][0]['label']
                    print('label: ', df_result.loc[i,'label'])
                if str('year') in response_json['results'][0].keys():
                    df_result.loc[i,'year'] = response_json['results'][0]['year']
                    print('year: ', df_result.loc[i,'year'])
                if str('country') in response_json['results'][0].keys():    
                    df_result.loc[i,'country'] = response_json['results'][0]['country']
                    print('country: ', df_result.loc[i,'country'])
                if str('community') in response_json['results'][0].keys():    
                    df_result.loc[i,'community'] = str(response_json['results'][0]['community'])
                    print('community: ', df_result.loc[i,'community'])
        print("\n")

    return df_result