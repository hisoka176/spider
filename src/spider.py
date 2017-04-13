#encoding=utf-8
import sys
from imp import reload
reload(sys)
import os
import re
'''
Created on 2017年3月15日

@author: libin_m
'''

from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import logging
import traceback
import pymysql

filename=r"E:\eclipse_workspace\eclipse\spider\logging.txt"
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
logging.basicConfig(filename=filename,format=fmt,level=logging.DEBUG)

global url_set
global cursor
global db
global need_url
db = pymysql.connect(host="localhost",user="root",passwd="root",db="hisoka_test",charset='utf8')
cursor = db.cursor()

cursor.execute('SET NAMES utf8;') 
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')


url_set = set()

logger = logging.getLogger()
need_url = re.compile('tl3d\.changyou\.com')

def liProcess(driver):
    global need_url
    print(driver.current_url)
    a = need_url.findall(driver.current_url)
    if not a:
        return 
    global cursor
    try:
        WebDriverWait(driver=driver,timeout=2).until(lambda x: x.find_element_by_css_selector("div.contentInner"))
        div = driver.find_element_by_css_selector("div.contentInner")
        title = div.find_element_by_tag_name("h1")
        time = div.find_element_by_css_selector("div.infos > div.time")
        content = driver.find_element_by_xpath("//div[@id='zoom']")
        
        sqlString = '''insert into tlbb(url,title,publish_data,content)
                    values('{0}','{1}','{2}','{3}')'''.format(driver.current_url,title.text,time.text,content.text.replace('\n','\t'))
        try:
            cursor.execute(sqlString)
            db.commit()
        except:
            logging.debug(traceback.format_exc())
            db.rollback()
            db.close()
        
        
        
    except Exception:
        logger.DEBUG(Exception.message)
    finally:
        return
          



def eachPage(driver):
    
   
    
    driver.implicitly_wait(1)
    ul = driver.find_element_by_css_selector("ul.news_list")
    lies = ul.find_elements_by_tag_name("li")
    for i in lies:
        driver.implicitly_wait(0.5)
        a_href = i.find_element_by_tag_name('a')
        a_href.click()
            
    time.sleep(2)
    main_handler = driver.current_window_handle
    
  
        
    for handler in driver.window_handles:
        if main_handler==handler:
            continue
        
        try:
            driver.switch_to_window(handler)
            liProcess(driver)
            driver.close()
        except:
            driver.close()
            continue
        
        
    driver.switch_to_window(main_handler)
     
    
    div = driver.find_element_by_css_selector("div.xtlPage")
    a4 = div.find_elements_by_tag_name("a")
    a4=a4[2]
    
    try:
        a4.click()
    except:
        exit(0)    
    return driver

def main():
 
    driver=webdriver.Chrome()
    driver.get("http://tl3d.changyou.com/tl3d/event/event_5.shtml")
    for i in range(16):
        driver = eachPage(driver)
        
 
def test1():
    driver = webdriver.Chrome()
    driver.get("http://tl3d.changyou.com/tl3d/event/event_16.shtml")
    content = driver.find_element_by_css_selector("div.xtlPage")
    tag_a = content.find_elements_by_tag_name("a")
    tag_a = tag_a[2]
    tag_a.click()
   
    
    
if __name__=='__main__':
    main()
   

    