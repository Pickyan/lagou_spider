#coding:utf-8

import requests
from bs4 import BeautifulSoup
import bs4
import threading
import time
import json
import chardet  #chardet.detect(str)查看字符串的编码格式

#repr() 函数将对象转化为供解释器读取的形式。

url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_python?px=default&city=%E4%B8%8A%E6%B5%B7',
    'X-Anit-Forge-Code':'0',
    'X-Anit-Forge-Token':None,
    'X-Requested-With':'XMLHttpRequest'
}

def get_page():
    pages_content = []
    for item in range(1,11):
        data = {
            'first': 'true',
            'pn':str(item),
            'kd': 'python'
        }
        page = requests.post(url,headers=headers,data=data)
        page_json = page.json()
        results = page_json['content']['positionResult']['result']
        for item in results:
            print(item['companyShortName'])
            positions = {
                'positionName':item['positionName'],
                'companyShortName':item['companyShortName'],
                'education':item['education'],
                'workYear':item['workYear'],
                'salary':item['salary'],
            }
            positionId = item['positionId']
            detail = position_detail(str(positionId))
            positions['detail'] = detail
            pages_content.append(positions)
        time.sleep(60)
    try:
        line = json.dumps(repr(pages_content),ensure_ascii=False) #json.dumps：将 Python 对象编码成 JSON 字符串。所以，此时的line是json字符串
    except:
        print('try里面运行不成功')
        pass
    with open('lagou.json', 'a', encoding='utf-8') as f:
        f.write(line)
    f.close()


def position_detail(id):
    url = 'https://www.lagou.com/jobs/%s.html'%id
    headers = {
        'Host':'www.lagou.com',
        'Referer':'https://www.lagou.com/jobs/list_python?px=default&city=%E4%B8%8A%E6%B5%B7',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html,'lxml')
    tar = soup.find('dd',attrs={'class':'job_bt'})
    if isinstance(tar, bs4.element.Tag):

        targ = tar.find_all('p')
        f = []
        for item in targ:
            if item.text:
                f.append(item.text)
        f1 = ''.join(f)
        return f1



# def main():
#     # for x in range(2):
#     #     th = threading.Thread(target=get_page)
#     #     th.start()
#     #     th.join()
#
#     get_page()

if __name__ == '__main__':
    # print('开始运行：')
    # a = position_detail(2848943)
    # print(a)

    th = threading.Thread(target=get_page)
    th.start()
    # th.join()

    # get_page()
