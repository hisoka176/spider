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

logging.basicConfig(filename='logger.text', level=logging.INFO)

## divide all url
class Stack(object):

    def __init__(self,lock,regex):

        self.stack = list()
        self.count = 0
        self.lock = lock
        self.urlCollection = set()
        self.regex = regex

        def addUrl(self,url):
            with lock:
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
            with self.lock:

                if len(self.stack)==0:
                    url=''
                else:
                    url=self.stack[0]
                    del self.stack[0]
                    return url
## get all url,process text
class WebPage(multiprocessing.Process):
        def __init__(self,stack,url):
            self.stack = stack
            self.url = url
            multiprocessing.Process.__init__(self)
            self.driver = webdriver.Chrome()
        def run(self):
            self.driver.get(self.url)
            tagAes = self.driver.find_elements_by_tag_name('a')
            for tagA in tagAes:
                url = tagA.get_property("a")
                self.tack.putUrl(url)

# lock
lock = multiprocessing.Lock()
# the url regex
regex = re.compile('https?:\/\/[a-z]+?\.sohu.com\/.*\.s?html')
# stack struct
stack = Stack(lock,regex)
# chrome driver
driver = webdriver.Chrome()
driver.get("http://www.sohu.com")
tagAes = driver.find_elements_by_tag_name("a")
for aElement in tagAes:
    url = aElement.get_property('href')
    stack.addUrl(url)
    driver.quit()
    for j in range(4):
        pool = list()
        for i in range(4):
            url = stack.getUrl()
            print(url)
            pool.append(WebPage(stack,url))
            for process in pool:
                process.start()

            for process in pool:
                process.join()
