import requests
import re
import time
from snownlp import SnowNLP
from bs4 import BeautifulSoup

header_str = '''
Cookie: bid=qslPNVL8KVE; __yadk_uid=x6rMxdAg7B0u2dVOsdLMtrQWTQ4ifElh; _vwo_uuid_v2=D152A61B581FDD37976848D468E756774|92395dde9e00d52279fb0d6e8f46e567; viewed="1438874"; push_doumail_num=0; push_noty_num=0; __utmv=30149280.22572; ll="128485"; vtd-d="1"; __gads=ID=2381e087574308dd-2230234b8dc400c3:T=1604501955:RT=1604501955:S=ALNI_MamiTf9uZ4-JB2Wp5Oxnw29u_WcYw; ct=y; __utmz=30149280.1604674290.33.23.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1604674309.31.22.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1604718768%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.617646310.1599931039.1604684564.1604718768.35; __utmb=30149280.0.10.1604718768; __utmc=30149280; __utma=223695111.307071430.1600620354.1604684564.1604718768.33; __utmb=223695111.0.10.1604718768; __utmc=223695111; dbcl2="225727052:Bu+qHVn9bWY"; ck=66Ds; _pk_id.100001.4cf6=b17b83d1d584e666.1600620354.33.1604719370.1604684570.
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
my_headers['Accept-Encoding'] = 'gzip'

film_id = {
           #'哪吒之魔童降世': '26794435',
           '流浪地球': '26266893',
           '复仇者联盟4：终局之战': '26100958',
           '我和我的祖国': '32659890',
           '中国机长': '30295905',
           '疯狂的外星人': '25986662',
           '飞驰人生': '30163509',
           '烈火英雄': '30221757',
           '少年的你': '30166972',
           '速度与激情：特别行动': '27163278'}


try:

    for movie in film_id:
        postive = 0
        netural = 0
        negative = 0
        with open(movie+'.txt', 'w', encoding='utf-8') as f:
            for page in range(0, 20):
                r = requests.get("https://movie.douban.com/subject/"+film_id[movie]+"/comments?start=" + str(20*page) +"&limit=20&status=P&sort=new_score", headers=my_headers)
                print(r.url)
                soup = BeautifulSoup(r.text, 'html.parser')
                all_comments = soup.find_all('span', 'short')

                for comment in all_comments:
                    print('正在读取第{0}页第{1}条评论...'.format(page+1, all_comments.index(comment)+1))
                    Chinese = re.sub(re.compile(r'[^\u4e00-\u9fa5]'), '', comment.string)
                    if(len(Chinese) != 0):
                        score = SnowNLP(Chinese).sentiments
                        if score >= 0.97:
                            f.write(str(score)+' '+str(1)+' '+comment.string+'\n\n')
                            postive += 1
                        elif score >= 0.92:
                            f.write(str(score)+' '+str(0)+' '+comment.string+'\n\n')
                            netural += 1
                        else:
                            f.write(str(score) + ' ' + str(-1) + ' ' + comment.string + '\n\n')
                            negative += 1
                    else:
                        score = 0
                        f.write(str(score) + ' ' + str(0) + ' ' + comment.string + '\n\n')
                        netural += 1
                time.sleep(2)
            print(postive, netural, negative)
            f.write('postive = '+str(postive)+'\nnetural = ' +str(netural)+'\nnegative = '+str(negative))
except:
    print('爬取失败')
