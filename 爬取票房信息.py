import requests
import re
import time
import json
from bs4 import BeautifulSoup
import xlwt

header_str = '''
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36
'''

def str_to_dict(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            li2[0] = li2[0].replace(':', '')
            res[li2[0]] = li2[1]
    return res

my_headers = str_to_dict(header_str, '\n', ': ')
try:
    r = requests.get("http://piaofang.maoyan.com/mdb/rank/query?type=0&id=2019", headers=my_headers)
    print(r.url)
    x = json.loads(r.text)['data']['list']
    for movie in x:
        print('{i}|{a}|{b}|{c}|{d}|{e}'.format(
            i=x.index(movie)+1,
            a=movie['movieName'],
            b=movie['releaseInfo'],
            c=movie['boxDesc'],
            d=movie['avgViewBoxDesc'],
            e=movie['avgShowViewDesc']
        ))
    time.sleep(2)
except:
    print('爬取失败')