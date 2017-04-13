#encoding=utf-8
import sys
from imp import reload
from inspect import stack
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
import multiprocessing

## 分发所有的url，加入url需要提供判重算法，共享变量，需要加锁
class Stack(object):
    
    def __init__(self,init=10):
        
        self.stack = list()
        self.count = 0
        
    def addUrl(self,url):
        
        pass
    
    def getUrl(self):
        
        pass
    

class UrlModel(object):
    
    def __init__(self,driver):
        
        self.driver = driver
         
    ## 得到所有的url
    def getAllUrl(self):
        
        tagA = self.driver.find_elements_by_tag_name("a")
        for i in tagA:
            print(i)
            
    def getAllText(self):
        
        
        pass
    
def main():
    driver = webdriver.Chrome()
    driver.get("http://www.sohu.com/")
    urlModel = UrlModel(driver)
    urlModel.getAllUrl()
        
    
if __name__=='__main__':
    main()

