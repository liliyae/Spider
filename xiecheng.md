## 携程景点图片和基本描述信息

景点图片链接中不含加密字段，网页编号顺序增加，可以构造链接，缺点是图片的分辨度不高。
```python
import sys
import requests
import json
import urllib as UrlUtils
from bs4 import BeautifulSoup
import random
import ast
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import openpyxl
import urllib
import requests
import time

def request(num):
    # 设置浏览器头部信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    url = 'https://you.ctrip.com/sight/qingdao5/s0-p'+str(num)+'.html' # 需要请求的网页的链接
    html = requests.get(url,headers=headers)  # get方式请求数据
    # print(html.status_code)  # 查看请求的状态码（200表示请求正常）
    html.encoding = 'utf-8'  # 设置编码，防止由于编码问题导致文字错乱
    # print(html.text)  # 查看请求到的内容
    content = html.text
    return content


k=21
while(k<86):
    k = k + 1
    data = openpyxl.load_workbook('xiecheng.xlsx')
    sheetnames = data.get_sheet_names()
    table = data.active
    nrows = table.max_row  # 获得行数

    con =request(k)
    soup = BeautifulSoup(con, "html.parser")

    # 获取所有的文章信息
    div_list = soup.find_all("div", class_="blogs")  # 注意： 若属性名是 class 则需要在后面加个下划线,写成 class_
    #print(soup.text)
    # items 是一个 <listiterator object at 0x10a4b9950> 对象，不是一个list，但是可以循环遍历所有子节点。
    #items = soup.find(attrs={'class': 'list_wide_mod2'}).children
    items = soup.find_all(attrs={'class': 'list_mod2'})
    projectList = []
    i = nrows+1
    for item in items:
       #if item == '\n': continue
       # 获取需要的数据
       #image=item.find_all('img')[1].text
       #table.cell(i, 1).value = image
       #if item.find_all('dd')!=None:
            name = item.find_all('a')[1].text
            table.cell(i, 1).value = name

            dd = item.find_all('dd')[0].text
            table.cell(i, 2).value = dd

            price = item.find_all('span')[1].text
            table.cell(i, 3).value = price

            score =item.find_all('a')[2].text
            table.cell(i, 4).value = score

            commentnum=item.find_all('a')[3].text
            table.cell(i, 5).value = commentnum

            img_url = item.find('img').attrs.get('src')
            print(img_url)
            # 下载图片
            r = urllib.request.urlretrieve(img_url, 'D:\\touristapp\\携程景点图片\\%s.jpg' % name)

            try:
                comment = item.find_all('p')[0].text
                table.cell(i, 6).value = comment
            except Exception:
                continue

            i = i+1
    data.save("xiecheng.xlsx")

```
