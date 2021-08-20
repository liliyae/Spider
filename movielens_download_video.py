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

options = webdriver.ChromeOptions()
# 添加UA
options.add_argument(
    'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
# 指定浏览器分辨率
options.add_argument('window-size=1920x3000')
# 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--disable-gpu')
# 隐藏滚动条, 应对一些特殊页面
options.add_argument('--hide-scrollbars')
# 不加载图片, 提升速度
options.add_argument('blink-settings=imagesEnabled=false')
# 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_argument('--headless')
# 以最高权限运行
options.add_argument('--no-sandbox')
# 设置开发者模式启动，该模式下webdriver属性为正常值
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 禁用浏览器弹窗
prefs = {
    'profile.default_content_setting_values': {
        'notifications': 2
    }
}
options.add_experimental_option('prefs', prefs)

browser = webdriver.Chrome(executable_path="D:\\tools\\chromedriver.exe",chrome_options=options)
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

