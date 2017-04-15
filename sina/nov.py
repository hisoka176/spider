#encoding=utf-8
import sys
from imp import reload
reload(sys)
import os
import re
'''
Created on 2017��3��15��

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
import pymysql
 

def main():
    """http://sax.sina.com.cn/dsp/click?
 t=MjAxNy0wNC0xNSAyMjowMjo1MS4xMjQJMTExLjIwNi4xMi4yMgkxMTEuMjA2LjEyLjIyXzE0OTIyNjM5
 NDYuNDg5MzQyCWU4YzQ1ZDllLTQzYzMtNGNkZS1iZTdkLWY5NWYyNjkwMjg3NQk3Njg5NjgJNTgyM
 zc2Nzk2NF9QSU5QQUktQ1BDCTI3NDk1MgkxMjU5NjcJMy41NDYwOTkyRS00CTEJdHJ1ZQlQRFBTMDA
 wMDAwMDU3NTMyCTE4OTIyNTUJUEMJaW1hZ2UJLQkwfDdBUzRvQ29VeW9NRkF5bGJVTHhGT3R8bn
 VsbHxudWxsfGJqfDc2ODk2OHwyeUZMaEZLY1BBNkkzOUJrRUdIektwCW51bGwJMQktCS0JLQkwCTEx
 MS4yMDYuMTIuMjJfMTQ5MjI2Mzk0Ni40ODkzNDIJUENfSU1BR0UJLQl1dmZtLXJ0CS0=&userid=111.
 206.12.22_1492263946.489342&auth=22f4122675f21845&p=CgJCTkjnPRmRLEENmY%2B57QZ1%
 2FJDanmhVqklAEA%3D%3D&url=http%3A%2F%2Fsax.sina.com.cn%2Fclick%3Ftype%3D2%26t%
 3DMGEwMjQyNGUtNDhlNy0zZDE5LTkxMmMtNDEwZDk5OGZiOWVkCTE3CVBEUFMwMDAwMDAwNTc
 1MzIJMTg5MjI1NQkxCVJUQgkt%26id%3D17%26url%3Dhttp%253A%252F%252Fpolariszg.com%
 252F%253Fgzid%253D7-180*150%26sina_sign%3Db02c5b885505b13a&sign=1db3016eca2f39cb"""
    
    

if __name__=='__main__':
    
    main()