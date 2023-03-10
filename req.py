#!/usr/bin/env python3
#-*- coding: utf-8-*-
import re
import sys
import requests
import warnings

warnings.filterwarnings("ignore")

class REQ:
    def __init__(self, url):
        self.url = url
        self.headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0(compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
                'Upgrade-Insecure-Requests':'1','Connection':'keep-alive','Cache-Control':'max-age=0',
                'Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8',
                "Referer": "https://www.baidu.com/"
        }

    def get_header(self):
        try:
            r = requests.head(self.url, headers=self.headers, verify=False, timeout=2)
            return r.status_code, r.headers
        except:
            return 0, []

    def get_content(self):
        try:
            r = requests.get(self.url, headers=self.headers, verify=False, timeout=10)
            body = r.text
            return body
        except:
            #print(sys.exc_info())
            return ""

    def get_json(self):
        try:
            r = requests.get(self.url, headers=self.headers, verify=False, timeout=20)
            body = r.json()
            return body
        except:
            return []

    def get_info(self):
        try:
            r = requests.get(self.url, headers=self.headers, verify=False, timeout=10)
            status = r.status_code
            headers = r.headers
            if r.encoding:
                text = r.text.encode(r.encoding).decode("utf-8").replace("\r", "").replace("\n", "") 
            else:
                text = r.text.replace("\r", "").replace("\n", "") 
            title=re.findall(r"<\s*title\s*>\s*([^<]+)\s*<\s*\/title\s*>",text[:10000])
            if len(title) != 0:
                return status, headers, title[0].strip(), text
            else:
                return status, headers, "", text
        except:
            #print(sys.exc_info())
            return "", "", "", ""