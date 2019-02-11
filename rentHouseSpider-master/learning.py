
#@Author:saviour_zjf
#@Date:2019/2/10 13:35
#@Name: practice how to use requests + BeautifulSoup

from bs4 import BeautifulSoup as qq
import requests

headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

r = requests.get('http://news.zhku.edu.cn/xxyw.htm',headers = headers)
r.encoding = 'utf-8'
r.soup = qq(r.text,"html.parser")
f = r.soup.find_all(lambda tag:tag.has_attr('title'))
print(f)








