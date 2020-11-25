import discogs_client
import pandas as pd
import time
import requests
import json



df = pd.read_csv("YT_liked_videos_2019-08-21.csv")

# Consumer Key	xsvlQuYcSWCicyBvwpXR
# Consumer Secret	aejCRjXyqebtqemXwChfKISWRHHifkjG

df_result = pd.DataFrame(columns=['styles','label','year','country','community'])

df = df['video_title']
search_n = len(df)
print("\n----------------------\n Search to process: ", search_n, "\n----------------------\n")

for i,title in enumerate(df):
    print(i, " - Still ", search_n - i , " to process")
    
    link = "https://api.discogs.com/database/search?q=" + str(title) + "&key=xsvlQuYcSWCicyBvwpXR&secret=aejCRjXyqebtqemXwChfKISWRHHifkjG"
    
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

df_result.to_csv('likedYT_DGSinfos.csv')