#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import models as mo
from selenium import webdriver
from datetime import date
import os

parser = argparse.ArgumentParser(description='Get playlist from YT',
                                epilog="easy and fast!")
parser.add_argument('-l', '--link', type=str,  
                    help='provide the playlist link')
parser.add_argument('-t','--timesleep', type=int,
                    help='provide the time sleep (default 3)')
parser.add_argument('-n','--nvideos', type=int,
                    help='provide the number of videos (default 100)')

args = parser.parse_args()

timesleep = 3
nvideos = 100

link = args.link
if args.timesleep:
    timesleep = args.timesleep
if args.nvideos:
    nvideos = args.nvideos

path = os.getcwd() + '/chromedriver'
os.chmod(path, 755)
driver = webdriver.Chrome(path)


if __name__ == '__main__':

    playlistname, df = mo.get_playlist(driver,link,nvideos,timesleep)
    df.to_csv( playlistname + ' - ' + str(date.today()) +'.csv')

    