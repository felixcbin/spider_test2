#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from pathlib import Path


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(my_dir + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            # filter out keep-alive new chunks
            if chunk:
                f.write(chunk)
                f.flush()

    return local_filename


headers = {  # 伪装浏览器
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/32.0.1700.76 Safari/537.36'
}

web_link = r"http://mebook.cc/"
root_link = r"https://www.yiyiclub.com/suxiongmote/27627.html"
my_dir = "D:/felix/"


def main():
    my_path = Path(my_dir)
    if not my_path.exists():
        os.makedirs(my_path)
    var = 1
    pool = Pool(8)
    while var == 1:
        req = requests.get(web_link, headers=headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text)
            print(soup.prettify())
            links = soup.find_all("ul")
            print(links)
            links = [l for l in links if l.get("class")]
            # for link in links:
            #     print(link.get("class"))
            sub_links = [l for l in links if (l.get("class")[0].find("sub") >= 0)]
            all_links = []
            for l in sub_links:
                all_links.append(re.findall(r'<a href=(.*?)</a>', str(l), re.S))
            # sub2_links = [re.findall(r'<a href=(.*?)</a>', l, re.S) for l in sub_links]
            # all_links = [((info.split(">")[0][1:-1], info.split(">")[1]) for info in l) for l in tmp_list]
            for urls in all_links:
                for url in urls:
                    kv = (url.split(">")[0][1:-1], url.split(">")[1])
                    req2 = requests.get(kv[0], headers=headers)
                    if req2.status_code == 200:
                        soup2 = BeautifulSoup(req2.text)
                        print(soup2.prettify())
                        all_divs = soup2.find_all("div")
                        all_divs = [div for div in all_divs if div.get("id")]
                        print(all_divs)
                        ids = [div.get("id") for div in all_divs if div.get("id")]
                        print(ids)
                        d_divs = [div for div in all_divs if div.get("id").find("primary") >= 0]
                        print(d_divs)
                        break
                break

            results = pool.map(download_file, links)
            next_link = soup.find_all('a')
            my_link = \
                [l.get("href") for l in next_link if re.match(r'^[0-9]', l.get("href").split('/')[-1], re.M | re.I)][0]
            if my_link.find("/"):
                my_link = web_link.split('/')[-1] + my_link
            else:
                my_link = web_link + my_link

            print("all download finished\n")
            var = 2


if __name__ == '__main__':
    main()
