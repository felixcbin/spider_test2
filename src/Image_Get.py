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
# root_link = r"http://www.cs.princeton.edu/~wayne/kleinberg-tardos/"
# root_link = r"https://www.ishsh.com/siwa/"
web_link = r"https://www.yiyiclub.com/suxiongmote/"
root_link = r"https://www.yiyiclub.com/suxiongmote/27627.html"
my_dir = "D:/felix/"


def main():
    my_path = Path(my_dir)
    if not my_path.exists():
        os.makedirs(my_path)
    var = 1
    my_link = root_link
    pool = Pool(8)
    while var == 1:
        req = requests.get(my_link, headers=headers)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text)
            print(soup.prettify())
            links = soup.find_all('img')
            print(links)
            # links = [l.get("data-original") for l in links if l.get('data-original')]
            links = [l.get("src") for l in links if l.get("id")]
            # pdf_links = [l.split("src=")[1] for l in links if l.endswith(".jpg")]
            # pdf_links = [l.index(1) for l in links if l.endswith(".jpg")]

            results = pool.map(download_file, links)
            next_link = soup.find_all('a')
            my_link = [l.get("href") for l in next_link if re.match(r'^[0-9]', l.get("href").split('/')[-1], re.M | re.I)][0]
            if my_link.find("/"):
              my_link = web_link.split('/')[-1] + my_link
            else:
              my_link = web_link + my_link

            print("all download finished\n")


if __name__ == '__main__':
    main()
