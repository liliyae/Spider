# For research
# video pages url is obtained by movielens.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import time
import random
import json
import urllib.request


browser = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe")
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 5) # 等待加载10s

team = {}

def login():
    with open('videopage.txt', 'r', newline='') as fb:
        lines = fb.readlines(1000)
        i = 0
        while(i<len(lines)+1):
            get_page_index(lines[i+1],lines[i])
            i = i + 2

def get_page_index(url,index):

    browser.get(url)
    try:
        time.sleep(5)
        html = browser.execute_script("return document.documentElement.outerHTML")
        #print(html)  # 输出网页源码

        class_name = 'video-player__video'
        pic = browser.find_element_by_class_name(class_name)
        disqus_pic = pic.find_element_by_tag_name('video')
        pic_url = disqus_pic.get_attribute('src')
        print(pic_url)
        index = index[:-2]
        urllib.request.urlretrieve(pic_url,"./video/"+index+".mp4")



    except Exception as e:
        print(str(e))


login()
