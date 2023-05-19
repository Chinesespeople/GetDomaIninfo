#!/usr/bin/env python3
#-*- coding: utf-8-*-
import re
import subprocess
import argparse
import time
import tkinter as tk
from bs4 import BeautifulSoup
from req import REQ
from concurrent.futures import ThreadPoolExecutor
    
def getDomainInfo(domainStr):
    try:
        chinazurl ="http://seo.chinaz.com/"+domainStr
        r = REQ(chinazurl)
        body = r.get_content()
        soup = BeautifulSoup(body)

        """
        取单位名称
        """
        elements = soup.find_all(id="company")
        start = str(elements[0]).find("<i class=\"color-63\">") + len("<i class=\"color-63\">")
        end = str(elements[0]).find("</i>")
        sub_str = str(elements[0])[start:end]
        sub_str = sub_str.replace(" ","").replace("\r\n","")
        compname = sub_str
        
        """
        取单位性质
        """
        comptpye = re.findall("<i class=\"color-63\">(.*)</i>", body)[0]

        """
        判断单位性质
        """
        if comptpye == "企业" or "-s-" in compname:
            compname = re.findall("//data.chinaz.com/company/([^\"]+)\"", compname)[0]
            compname = compname.split('-')[-1]

        """
        获取百度权重
        """
        try:
            result = subprocess.run('curl -i "https://baidurank.aizhan.com/api/br?domain={0}&style=images"'.format(domainStr), stdout=subprocess.PIPE,stderr=False, shell=True)
            baiduvar = re.findall('https://statics.aizhan.com/images/br/(.*).png', str(result.stdout))[0]
        except:
            baiduvar = ""

        """
        获取备案号
        """
        try:
            links = soup.find_all('a', {'href': '//icp.chinaz.com/'+domainStr})
            icpcontent = links[0].get_text()
        except:
            icpcontent = ""

        """
        获取域名IP对应信息
        """
        try:
            links = soup.select('a[href*="//ip.tool.chinaz.com/?ip="]')
            domainIP = links[0].get_text()
        except:
            domainIP = ""
    except:
        compname = ""
        comptpye = ""
        baiduvar = ""
        icpcontent = ""
        domainIP = ""
    return baiduvar,domainStr,compname,comptpye,icpcontent,domainIP

def initdomain(domainstr):
    if "//" in domainstr:
        domainstr = domainstr[str(domainstr).index("//")+2:]
    if "/" in domainstr:
        domainstr = domainstr[:str(domainstr).index("/")]
    if ":" in domainstr:
        domainstr = domainstr[:str(domainstr).index(":")]
    return domainstr

if __name__=="__main__":
    parser = argparse.ArgumentParser(description=
                                     """
                                     Get Domain Information
                                     """
                                     )
    parser.add_argument('--file','-f', help='设置一个域名列表文件，该文件每一行应该为一个域名格式的字符串。默认为当前目录下的test.txt。')
    parser.add_argument('--output','-o', help='指定输出的csv文件名。不指定该参数程序将会将结果默认保存为[当前时间戳.csv]文件。')
    parser.add_argument('--threads','-t', help='指定线程数。默认为 1。')
    args = parser.parse_args()
    inputfile = "test.txt"
    outputfile = str(time.time())+".csv"
    thread_size = 1
    if args.file:
        inputfile = args.file
    if args.output:
        outputfile = args.output
    if args.threads:
        thread_size = int(args.threads)
    
    pool = ThreadPoolExecutor(max_workers=thread_size)
    filelines = open(inputfile).readlines()
    f = open(outputfile,"a+")
    f.write("百度权重,域名,单位名称,性质,ICP备案号,IP信息\n")
    f.close()
    for i in filelines:
        try:
            f = open(outputfile,"a+")
            result = pool.submit(getDomainInfo,i.replace("\n",""))
            print(result.result())
            f.write(str(result.result()[0])+","+str(result.result()[1])+","+str(result.result()[2])+","+str(result.result()[3])+","+str(result.result()[4])+","+str(result.result()[5])+"\n")
            f.close()
        except KeyboardInterrupt:
            print("Bye!~")
            break
