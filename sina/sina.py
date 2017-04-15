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

logging.basicConfig(filename='logger.text', level=logging.INFO)



## divide all url
class UrlStack(object):

    def __init__(self,lock,regex):

        self.stack = list()
        self.count = 0
        self.lock = lock
        self.urlCollection = set()
        self.regex = regex

    def addUrl(self,url):
        with self.lock:
            logging.info(url)
        # if the url has beed added,it neednot to added
            match = self.regex.match(url)
            if not match:
                return ''
            if url in self.urlCollection:
                return
            else:
                self.urlCollection.add(url)
                # add url
                self.count += 1
                self.stack.append(url)#
                
    def getUrl(self):
        print(self.stack[:3])
        with self.lock:

            if len(self.stack)==0:
                url=''
            else:
                url=self.stack[0]
                del self.stack[0]
                return url
            
def processUrl(stack,url):
       
    db = pymysql.connect(host="localhost",user="root",passwd="root",db="spider",charset='utf8')
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;') 
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    
    
    option = webdriver.ChromeOptions()
#     option.add_argument('--user-agent=iphone')
#     option.add_argument('--disable-plugins')
#     option.add_argument('--disable-javascript')
#     option.add_argument('--disable-plugins')
#     option.add_argument('--disable-images')
    
    option_path="--user-data-dir=d:/data/nova"
    option.add_argument(option_path)
    driver = webdriver.Chrome(chrome_options=option)
 
    driver.get(url)
    ## insert date into databases
    #content = WebDriverWait(driver=self.driver,timeout=2).until(lambda x: x.find_element_by_css_selector("div"))
    content =  driver.find_elements_by_tag_name("p")
    content = [i.text for i in content]
    text = ','.join(content)
 
 
    url =  driver.current_url
   
    sqlString = '''insert into pages (url,content) values ("{0}","{1}");'''.format(url,text)
    ## if failture db roll back  
    try:
        cursor.execute(sqlString)
        db.commit()
    except:
     
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
        stack.addUrl(url)
    
    driver.close()
 

if __name__=='__main__':
    lock = multiprocessing.Lock()
    # the url regex
    regex = re.compile('https?:\/\/www.sina.com.*?\.html')
    # stack struct
    stack = UrlStack(lock,regex)
    
    option = webdriver.ChromeOptions()
#     option.add_argument('--user-agent=iphone')
#     option.add_argument('--disable-plugins')
#     option.add_argument('--disable-javascript')
#     option.add_argument('--disable-plugins')
#     option.add_argument('--disable-images')
    
    option_path="--user-data-dir=d:/data/nova"
    option.add_argument(option_path)
    driver = webdriver.Chrome(chrome_options=option)
    
    # chrome driver
    
    driver.get("http://www.sina.com")
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
     
    url = stack.getUrl()
    pro1 = multiprocessing.Process(target=processUrl,args=(stack, url))
    url = stack.getUrl()
    pro2 = multiprocessing.Process(target=processUrl,args=(stack, url))
     
    
     
    pro1.start()
    pro2.start()
    
    pro1.join()
    pro2.join()
