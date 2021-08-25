#!/usr/bin/env python
# -*- coding:utf-8 -*-
#for research progress
import urllib
import os
import time
import re
import logging
import requests
import urllib3
import threading
# json解析库,对应到lxml
import json
# 全局取消证书验证
import io
import sys
import _thread
# 改变标准输出的默认编码
# utf-8中文乱码 有些表情print不进去
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import openpyxl
import socket


def req_open_html(url):
    print('req_open_html begin')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
    request = urllib.request.Request(url, headers=headers)
    NET_STATUS = False
    while not NET_STATUS:
        try:
            html = urllib.request.urlopen(request, data=None, timeout=3).read().decode('utf-8')
            print('NET_STATUS is good')
            print('req_open_html end')
            return html

        except socket.timeout:
            print('NET_STATUS is not good')
            NET_STATUS = False
            pass

def req_open_mvurl(url,id):
    global flag

    flag = False
    print('req_open_html begin')
    NET_STATUS = False
    while not NET_STATUS:
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent",
                                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url,'/home/share/xiaotianshu/douyin/video/%s.mp4' % str(id))
            break

            print('NET_STATUS is good')
            print('req_open_mvurl end')

        except socket.timeout:
            print('NET_STATUS is not good')
            NET_STATUS = False
    flag = False

def req_open_musicurl(url,id):
    global flag

    print('req_open_html begin')

    NET_STATUS = False
    while not NET_STATUS:
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent",
                                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url,'/home/share/xiaotianshu/douyin/music/%s.mp3' % str(id))
            break

            print('NET_STATUS is good')
            print('req_open_musicurl end')

        except socket.timeout:
            print('NET_STATUS is not good')
            NET_STATUS = False
    flag = False

def timess(url1,url2,vid,mid):
    global flag
    flag = True
    _thread.start_new_thread(req_open_mvurl, (url1,vid,))
    _thread.start_new_thread(req_open_musicurl, (url2,mid,))
    start_time = time.time()
    while time.time() - start_time < 30:
        if flag == False:
            print("parent terminated!")
            break
        else:
            time.sleep(2)

if __name__ == '__main__':
    # t = "https://www.iesdouyin.com/web/api/v2/challenge/aweme/?ch_id=1575530906796046&count=9&cursor=5250&aid=1128&screen_limit=3&download_click_limit=0&_signature=ceCrSgAALpeZOok3x3WA2nHgq1"
    first = "https://www.iesdouyin.com/web/api/v2/challenge/aweme/?ch_id=1575530906796046&count=50&cursor="
    last = "&aid=1128&screen_limit=3&download_click_limit=0&_signature=ceCrSgAALpeZOok3x3WA2nHji0"

    for i in range(1355, 8650):
        x = i * 50
        video_url = first + str(x) + last
        print(i)
        html = req_open_html(video_url)

        data = openpyxl.load_workbook('douyin0.xlsx')
        # 取第一张表
        sheetnames = data.get_sheet_names()
        table = data.get_sheet_by_name(sheetnames[0])
        table = data.active
        nrows = table.max_row  # 获得行数
        index = 1

        unicodestr = json.loads(html)

        user_list = unicodestr.get("aweme_list")
        if user_list != None:
            for eve in user_list:
                music = eve.get("music")
                if (music != None):
                    music_title = music.get("title")
                    if (music_title.find('@') != 0 and music_title != '用户创作的原声'):
                        music_playurls = music.get("play_url")
                        music_playurl = music_playurls.get("uri")
                        if (music_playurl != ''):
                            table.cell(nrows + index, 1).value = str(music_title)
                            music_anthor = music.get("author")
                            table.cell(nrows + index, 2).value = str(music_anthor)
                            temp = music.get("cover_medium")
                            music_pic = temp.get("url_list")
                            music_picture = music_pic[0]
                            table.cell(nrows + index, 3).value = str(music_picture)
                            table.cell(nrows + index, 4).value = str(music_playurl)

                            video = eve.get("video")
                            if (video != None):
                                download_suffix_logo_addr = video.get("play_addr")
                                video_id = video.get("vid")
                                if (download_suffix_logo_addr != None and video_id != None):
                                    url_list = download_suffix_logo_addr.get("url_list")
                                    if (url_list != None):
                                        mvurl = url_list[0]
                                        table.cell(nrows + index, 5).value = str(mvurl)
                                        _thread.start_new_thread(timess, (mvurl, music_playurl, video_id, music_title,))

                                        index = index + 1
        data.save('douyin0.xlsx')

        time.sleep(5)

    #douyin()

