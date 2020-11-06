import requests
import re
import time
from bs4 import BeautifulSoup

header_str = '''
Cookie: bid=qslPNVL8KVE; __yadk_uid=x6rMxdAg7B0u2dVOsdLMtrQWTQ4ifElh; _vwo_uuid_v2=D152A61B581FDD37976848D468E756774|92395dde9e00d52279fb0d6e8f46e567; viewed="1438874"; push_doumail_num=0; push_noty_num=0; __utmv=30149280.22572; ll="128485"; vtd-d="1"; __gads=ID=2381e087574308dd-2230234b8dc400c3:T=1604501955:RT=1604501955:S=ALNI_MamiTf9uZ4-JB2Wp5Oxnw29u_WcYw; ct=y; __utmc=30149280; __utmz=30149280.1604674290.33.23.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utmz=223695111.1604674309.31.22.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; dbcl2="225727052:aXdIq6m1FWM"; ck=kQjd; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1604684564%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=b17b83d1d584e666.1600620354.32.1604684564.1604675399.; _pk_ses.100001.4cf6=*; __utma=30149280.617646310.1599931039.1604674290.1604684564.34; __utmb=30149280.0.10.1604684564; __utma=223695111.307071430.1600620354.1604674309.1604684564.32; __utmb=223695111.0.10.1604684564
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
           #'流浪地球': '26266893',
           #'复仇者联盟4：终局之战': '26100958',
           #'我和我的祖国': '32659890',
           #'中国机长': '30295905',
           #'疯狂的外星人': '25986662',
           #'飞驰人生': '30163509',
           '烈火英雄': '30221757',
           '少年的你': '30166972',
           '速度与激情：特别行动': '27163278'}


header_str2 = '''
Cookie: bid=qslPNVL8KVE; __yadk_uid=x6rMxdAg7B0u2dVOsdLMtrQWTQ4ifElh; _vwo_uuid_v2=D152A61B581FDD37976848D468E756774|92395dde9e00d52279fb0d6e8f46e567; viewed="1438874"; push_doumail_num=0; push_noty_num=0; __utmv=30149280.22572; ll="128485"; vtd-d="1"; __gads=ID=2381e087574308dd-2230234b8dc400c3:T=1604501955:RT=1604501955:S=ALNI_MamiTf9uZ4-JB2Wp5Oxnw29u_WcYw; ct=y; __utmc=30149280; __utmz=30149280.1604674290.33.23.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utmz=223695111.1604674309.31.22.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; dbcl2="225727052:aXdIq6m1FWM"; ck=kQjd; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1604684564%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=b17b83d1d584e666.1600620354.32.1604684564.1604675399.; _pk_ses.100001.4cf6=*; __utma=30149280.617646310.1599931039.1604674290.1604684564.34; __utmb=30149280.0.10.1604684564; __utma=223695111.307071430.1600620354.1604674309.1604684564.32; __utmb=223695111.0.10.1604684564
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36
'''

my_headers2 = str_to_dict(header_str2, '\n', ': ')

my_headers2['Accept-Encoding'] = 'gzip'

try:
    for movie in film_id: #10部电影
        with open(movie + '.txt', 'w', encoding='utf-8') as f:
            print("正在爬取"+movie)
            distribution = {"unknown": 0, "国外": 0}
            for page in range(0, 20):
                print("正在爬取第{0}页".format(page+1))
                r = requests.get("https://movie.douban.com/subject/"+film_id[movie]+"/comments?start=" + str(20*page) +"&limit=20&status=P&sort=new_score", headers=my_headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                print(r.url)
                all_user = soup.find_all('a', href=re.compile(r'https://www.douban.com/people/\S+/'), title=False)
                all_user_href = re.compile(r'https://www.douban.com/people/.*?/').findall(str(all_user))
                for user in all_user_href:
                    user_page = requests.get(user, headers=my_headers2)
                    user_soup = BeautifulSoup(user_page.text, 'html.parser')
                    user_info = user_soup.find_all('div', 'user-info')
                    user_location = re.compile(r'>.*?</a').findall(str(user_info))

                    print('正在读取第{0}页第{1}条评论...'.format(page+1, all_user_href.index(user)+1))
                    if len(user_location) != 0:
                        location = user_location[0].split('>')[-1].split('<')[0]
                        if re.compile(r'[\u4e00-\u9fa5]').match(location) != None:
                            if location in distribution:
                                distribution[location] += 1
                            else:
                                distribution[location] = 1
                        else:
                            distribution["国外"] += 1;
                    else:
                        distribution["unknown"] += 1
                    time.sleep(2)
                time.sleep(2)
            for x in distribution:
                f.write(x+str(distribution[x]) + '\n\n')
except:
    print('爬取失败')