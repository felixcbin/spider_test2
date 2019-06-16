#coding:utf-8
import re
from urllib import request
from bs4 import BeautifulSoup
from urllib import error

from minfo_save import csvHandler, mysqlHandler

base_url = 'https://movie.douban.com/top250?start=%d&filter='

class spider_douban250(object):
    def __init__(self, url = None, start = 0, step = 25, total = 250, savehd=None):
        self.durl = url
        self.dstart = start
        self.dstep = step
        self.dtotal = total
        self.infohd = savehd

    def start_download(self):
        while self.dstart < self.dtotal:
            durl = self.durl%self.dstart
            self.load_page(durl)
            self.dstart += self.dstep
            break

            
    def req_page(self, url):
        try:
            req = request.urlopen(url)
        except error.HTTPError as e:
            print ('catch e:', e)
            return None
        except:
            print ('url request error:', url)
            return None

        if req.code != 200:
            return
        pageinfo = req.read().decode('utf-8')
        return pageinfo

    def parse_text(self, minfo):
        #listt = minfo.split('\n')
        print (minfo)
        listt = [item.strip() for item in minfo.split('\n') if item.strip(' ')]
        listt = [item.split(':', 1) for item in listt]
        listt = [items for items in listt if len(items)==2 and items[0].strip() and items[1].strip()]
        print (listt)
        dinfo = dict(listt)

        return dinfo


    def parse_minfo(self, url, mname):
        pinfo = self.req_page(url)
        if not pinfo:
            return
        obj = BeautifulSoup(pinfo, 'html5lib')
        minfo = obj.find('div', id='info')
        tinfo = minfo.get_text()
        dinfo = self.parse_text(tinfo)
        mscore = obj.find('div', class_='rating_self clearfix')
        score = mscore.find(property="v:average").get_text()
        votes = mscore.find(property="v:votes").get_text()
        dinfo['score'] = score
        dinfo['votes'] = votes
        dinfo['name'] = mname
        print (dinfo.keys())
        for item in dinfo.items():
            print(item)
        return dinfo


    def load_page(self, url):
        pinfo = self.req_page(url)
        if not pinfo:
            return
        obj = BeautifulSoup(pinfo, 'html5lib')
        listdiv = obj.find_all('div', class_='hd')
        for div in listdiv:

            murl = div.find('a').get('href')
            mname = div.find('span', class_='title').get_text()
            print (murl, mname)
            minfo = self.parse_minfo(murl, mname)
            if minfo and self.infohd:
                keys = ['name', '导演', '主演', '类型', '制片国家/地区',
                        '语言', '上映日期', '片长', '又名',
                        'score', 'votes']
                self.infohd.write(keys,minfo)


    def load_img(self, info):
        imgreq = request.urlopen(info[1])
        img_c = imgreq.read()
        imgf = open('F:\\test\\' + info[0] + '.jpg', 'wb')
        imgf.write(img_c)
        imgf.close()

fcsv = csvHandler('minfo.csv')
sql = mysqlHandler('localhost', 'root', 'abcd1234', 'test_db1', 'mvinfo')
# spider = spider_douban250(base_url, start=0, step=25, total=250, savehd = sql)
# spider.start_download()
fcsv.close()