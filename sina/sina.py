#! /usr/bin/env python3.5
import sys
from imp import reload
from inspect import stack
reload(sys)
import os
import re


from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import logging
import multiprocessing
import pymysql
import urllib
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
 

logging.basicConfig(filename='logger.text', level=logging.INFO)


def processString(url):
    if "\"" in url:
        url = url.replace('\"',',')
    if "\'" in url:
        url = url.replace('\'',',')
    return url
## divide all url
class UrlStack(object):

    def __init__(self,lock):

        self.stack = list()
        self.count = 0
        self.lock = lock
        self.urlCollection = set()
     
        self.urlList =   set([
        'news.sina.com.cn',
        'mil.news.sina.com.cn',
        'finance.sina.com.cn',
        'tech.sina.com.cn',
        'mobile.sina.com.cn',
        'tech.sina.com.cn',
        'sports.sina.com.cn',
        'ent.sina.com.cn',
        'astro.sina.com.cn',
        'auto.sina.com.cn',
        'dealer.auto.sina.com.cn',
        'data.auto.sina.com.cn',
        'blog.sina.com.cn',
        'zhuanlan.sina.com.cn',
        'baby.sina.com.cn',
        'esf.leju.com',
        'jiaju.sina.com.cn',
        'book.sina.com.cn',
        'history.sina.com.cn',
        'edu.sina.com.cn',
        'health.sina.com.cn',
        'fashion.sina.com.cn',
        'travel.sina.com.cn',
        'eladies.sina.com.cn',
        'sports.sina.com.cn',
        'news.sina.cn',
        'mil.news.sina.cn',
        'finance.sina.cn',
        'tech.sina.cn',
        'mobile.sina.cn',
        'tech.sina.cn',
        'sports.sina.cn',
        'ent.sina.cn',
        'astro.sina.cn',
        'auto.sina.cn',
        'dealer.auto.sina.cn',
        'data.auto.sina.cn',
        'blog.sina.cn',
        'zhuanlan.sina.cn',
        'baby.sina.cn',
        'jiaju.sina.cn',
        'book.sina.cn',
        'history.sina.cn',
        'edu.sina.cn',
        'health.sina.cn',
        'fashion.sina.cn',
        'travel.sina.cn',
        'eladies.sina.cn',
        'sports.sina.cn',
        'my.sina.cn',     
        'news.sina.cn',     
        'finance.sina.cn',     
        'sports.sina.cn',     
        'ent.sina.cn',     
        'mil.sina.cn',     
        'blog.sina.cn',     
        'eladies.sina.cn',     
        'games.sina.cn'  
     ])

    def addUrl(self,url):
        print(url)
        urlpath = urllib.parse.urlparse(url)
        if urlpath.netloc not in self.urlList:
            return 
        if url is None:
            logging.info('None error:' % (url))
            return 
        if 'click' in url:
            return 
        with self.lock:
             
        # if the url has beed added,it neednot to added
#             print(url)
           
            if url in self.urlCollection:
                return
            else:
                self.urlCollection.add(url)
                # add url
                self.count += 1
                self.stack.append(url)#
                if self.count > 100:
                    exit(0)
                
    def getUrl(self):
        print(self.stack[:10])
        with self.lock:

            if len(self.stack)==0:
                url=''
            else:
                url=self.stack[0]
                del self.stack[0]
                if url is None:
                    logging.info('2 None error:' % (url))
                return url
            
def processUrl(stack,url):
       
    db = pymysql.connect(host="localhost",user="root",passwd="root",db="spider",charset='utf8')
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;') 
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    


    driver = getChromeDriver()
 
    driver.get(url)
 
    content =  driver.find_elements_by_tag_name("p")
    content = [i.text for i in content]
    text = ','.join(content)
 
 
    url =  driver.current_url
    text = processString(text)
    sqlString = '''insert into pages (url,content) values ("{0}","{1}");'''.format(url,text)
    ## if failture db roll back  
    try:
        cursor.execute(sqlString)
        db.commit()
    except:
        logging.info('sql error %s' % (sqlString))
        db.rollback()
    finally:
        db.close()
               
    ## insert url into stack 
    tagAes = driver.find_elements_by_tag_name('a')
    if len(tagAes) == 0:
        return 
    for tagA in tagAes:
        url = tagA.get_property("a")
        text = tagA.text
        ## url is not string or byte-like object
        if tagA is None:
            continue
        stack.addUrl(url)
    
    driver.close()
 
def getFireFoxDriver():
    ## get the Firefox profile object
#     firefoxProfile = FirefoxProfile()
#     ## Disable CSS
#     firefoxProfile.set_preference('permissions.default.stylesheet', 2)
#     ## Disable images
#     firefoxProfile.set_preference('permissions.default.image', 2)
#     ## Disable Flash
#     firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
#                                   'false')
    ## Set the modified profile while creating the browser object 
#     options = webdriver.ChromeOptions()
#     # set language chinese
#     options.add_argument('lang=zh_CN.UTF-8')
#     # set header
#     options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
#     driver = webdriver.Firefox(firefox_profile=firefoxProfile)
    driver = webdriver.Firefox()
    return driver

def getChromeDriver():
#     option_path="--user-data-dir=d:/data/nova"
#     option.add_argument(option_path)
#     
#  
#     option.binary_location = r'C:/Program Files (x86)/Google/Chrome/Application'
#     service_log_path = "./chromedriver.log"
#     service_args = ['--verbose']
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    # set header
    options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
#     option.add_argument('--user-agent=iphone')
#     option.add_argument('--disable-plugins')
#     option.add_argument('--disable-javascript')
#     option.add_argument('--disable-plugins')
#     option.add_argument('--disable-images')
    
#     option_path="--user-data-dir=d:/data/nova"
#     options.add_argument(option_path)
#     driver = webdriver.Chrome(executable_path=r'C:/Windows/System32/chromedriver.exe',chrome_options=options)
    driver = webdriver.Chrome(chrome_options=options)
    return driver
 
if __name__=='__main__':
    lock = multiprocessing.Lock()
 
 
    # stack struct
    stack = UrlStack(lock)
    
    url="http://www.sina.com.cn"

    driver = getChromeDriver()
    
    driver.get(url)
 
    
#     driver.get("https://www.toutiao.com/ch/news_sports/")
    tagAes = driver.find_elements_by_tag_name("a")
     
    for aElement in tagAes:
        
        try:
            url = aElement.get_property('href')
            if url is None:
                continue
         
            stack.addUrl(url)
        except:
            pass
        finally:
            pass
        
    driver.close()
 
    
    pool = list()
    while True:
       
        url = stack.getUrl()
        process1 = multiprocessing.Process(target=processUrl,args=(stack, url))
        url = stack.getUrl()
        process2 = multiprocessing.Process(target=processUrl,args=(stack, url))
        url = stack.getUrl()
        process3 = multiprocessing.Process(target=processUrl,args=(stack, url))
        url = stack.getUrl()
        process4 = multiprocessing.Process(target=processUrl,args=(stack, url))
             
        process1.start()
        process2.start()
        process3.start()
        process4.start()
            
        process1.join()
        process2.join()    
        process3.join()    
        process4.join()    
         
    
