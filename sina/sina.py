{
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.2"
  },
  "name": ""
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "#! /usr/bin/env python3.5\n",
      "import sys\n",
      "from imp import reload\n",
      "from inspect import stack\n",
      "reload(sys)\n",
      "import os\n",
      "import re\n",
      "'''\n",
      "Created on 2017\u5e743\u670815\u65e5\n",
      "\n",
      "@author: libin_m\n",
      "'''\n",
      "\n",
      "from selenium import webdriver\n",
      "import unittest\n",
      "from selenium.webdriver.common.by import By\n",
      "import time\n",
      "from selenium.webdriver.common.keys import Keys\n",
      "from selenium.webdriver.support.ui import WebDriverWait\n",
      "from selenium.webdriver.support import expected_conditions as EC\n",
      "import unittest\n",
      "import logging\n",
      "import multiprocessing\n",
      "print('over')"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "ename": "SyntaxError",
       "evalue": "invalid syntax (<ipython-input-50-9003e8e3a421>, line 2)",
       "output_type": "pyerr",
       "traceback": [
        "\u001b[0;36m  File \u001b[0;32m\"<ipython-input-50-9003e8e3a421>\"\u001b[0;36m, line \u001b[0;32m2\u001b[0m\n\u001b[0;31m    export EDITOR=\"/usr//bin/emacs\u201d\u001b[0m\n\u001b[0m                ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
       ]
      }
     ],
     "prompt_number": 50
    },
    {
     "cell_type": "code",
     "collapsed": true,
     "input": [
      "logging.basicConfig(filename='logger.text', level=logging.INFO)"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 12
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "\n",
      "\n",
      "## \u5206\u53d1\u6240\u6709\u7684url\uff0c\u52a0\u5165url\uff0c\u9700\u8981\u52a0\u9501\n",
      "class Stack(object):\n",
      "    \n",
      "    def __init__(self,lock,regex):\n",
      "        \n",
      "        self.stack = list()\n",
      "        self.count = 0\n",
      "        self.lock = lock\n",
      "        self.urlCollection = set()\n",
      "        self.regex = regex\n",
      "        \n",
      "    def addUrl(self,url):\n",
      "        with lock:\n",
      "            logging.info(url)\n",
      "            # \u5bf9\u4e8e\u5df2\u7ecf\u63d0\u53d6\u7684\u9875\u9762\u4e0d\u518d\u63d0\u53d6\n",
      "            match = self.regex.match(url)\n",
      "            if not match:\n",
      "                return ''\n",
      "            if url in self.urlCollection:\n",
      "                return\n",
      "            else:\n",
      "                self.urlCollection.add(url)\n",
      "            # \u589e\u52a0url\n",
      "            self.count += 1\n",
      "            self.stack.append(url)\n",
      "    \n",
      "    def getUrl(self):\n",
      "        with self.lock:\n",
      "        \n",
      "            if len(self.stack)==0:\n",
      "                url=''\n",
      "            else:\n",
      "                url=self.stack[0]\n",
      "                del self.stack[0]\n",
      "        return url\n",
      "\n",
      "\n",
      "## \u529f\u80fd\u6dfb\u52a0\u7f51\u9875\uff0c\u5904\u7406\u6587\u672c\n",
      "class WebPage(multiprocessing.Process):\n",
      "    def __init__(self,stack,url):\n",
      "        self.stack = stack\n",
      "        self.url = url\n",
      "        multiprocessing.Process.__init__(self)\n",
      "        self.driver = webdriver.Chrome()\n",
      "    def run(self):\n",
      "        self.driver.get(self.url)\n",
      "        tagAes = self.driver.find_elements_by_tag_name('a')\n",
      "        for tagA in tagAes:\n",
      "            url = tagA.get_property(\"a\")\n",
      "            self.tack.putUrl(url)\n",
      "    "
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 48
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "# \u9501\n",
      "lock = multiprocessing.Lock()\n",
      "# \u8981\u722c\u53d6\u7f51\u9875\u7684url\u6b63\u5219\u8868\u8fbe\u5f0f\n",
      "regex = re.compile('https?:\\/\\/[a-z]+?\\.sohu.com\\/.*\\.s?html')\n",
      "# \u6808\u7ed3\u6784\n",
      "stack = Stack(lock,regex)\n",
      "# chrome\u9a71\u52a8\n",
      "driver = webdriver.Chrome()\n",
      "driver.get(\"http://www.sohu.com\")\n",
      "tagAes = driver.find_elements_by_tag_name(\"a\")\n",
      "for aElement in tagAes:\n",
      "    url = aElement.get_property('href')\n",
      "    stack.addUrl(url)\n",
      "driver.quit()\n",
      "for j in range(4):\n",
      "    pool = list()\n",
      "    for i in range(4):\n",
      "        url = stack.getUrl()\n",
      "        print(url)\n",
      "        pool.append(WebPage(stack,url))\n",
      "    for process in pool:\n",
      "        process.start()\n",
      "        \n",
      "    for process in pool:\n",
      "        process.join()\n",
      "    "
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "http://sports.sohu.com/nba.shtml\n",
        "http://sports.sohu.com/zhongchao.shtml\n",
        "http://sports.sohu.com/xijia.shtml\n",
        "http://learning.sohu.com/20170114/n478695279.shtml\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stderr",
       "text": [
        "Process WebPage-86:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-87:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-85:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-88:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "http://learning.sohu.com/20170113/n478588542.shtml\n",
        "http://learning.sohu.com/20170111/n478369304.shtml\n",
        "http://learning.sohu.com/20170116/n478797554.shtml\n",
        "http://mt.sohu.com/tags/182.shtml\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stderr",
       "text": [
        "Process WebPage-92:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-91:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 49, in run\n",
        "    tagAes = self.driver.find_elements_by_tag_name('a')\n",
        "  File \"/home/hisoka176/.local/lib/python3.5/site-packages/selenium/webdriver/remote/webdriver.py\", line 414, in find_elements_by_tag_name\n",
        "    return self.find_elements(by=By.TAG_NAME, value=name)\n",
        "  File \"/home/hisoka176/.local/lib/python3.5/site-packages/selenium/webdriver/remote/webdriver.py\", line 810, in find_elements\n",
        "    'value': value})['value']\n",
        "  File \"/home/hisoka176/.local/lib/python3.5/site-packages/selenium/webdriver/remote/webdriver.py\", line 249, in execute\n",
        "    self.error_handler.check_response(response)\n",
        "  File \"/home/hisoka176/.local/lib/python3.5/site-packages/selenium/webdriver/remote/errorhandler.py\", line 193, in check_response\n",
        "    raise exception_class(message, screen, stacktrace)\n",
        "selenium.common.exceptions.NoSuchWindowException: Message: no such window: target window already closed\n",
        "from unknown error: web view not found\n",
        "  (Session info: chrome=57.0.2987.133)\n",
        "  (Driver info: chromedriver=2.24.417424 (c5c5ea873213ee72e3d0929b47482681555340c3),platform=Linux 4.4.0-72-generic x86_64)\n",
        "\n",
        "Process WebPage-90:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-89:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "http://mt.sohu.com/tags/192.shtml\n",
        "http://tv.sohu.com/20170321/n484143076.shtml?%20channeled=1200340001\n",
        "http://film.sohu.com/album/9297294.html?channeled=1200340002\n",
        "http://tv.sohu.com/20170322/n484314068.shtml?%20channeled=1200340003\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stderr",
       "text": [
        "Process WebPage-95:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-94:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-96:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "http://film.sohu.com/album/9297251.html?%20channeled=1200340004\n",
        "http://www.sohu.com/house.focus.cn/daogou/11382695.html\n",
        "http://news.sohu.com/20170415/n488543319.shtml?fi\n",
        "http://news.sohu.com/20170414/n488473484.shtml?fi\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stderr",
       "text": [
        "Process WebPage-97:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-99:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n",
        "Process WebPage-100:\n",
        "Traceback (most recent call last):\n",
        "  File \"/usr/lib/python3.5/multiprocessing/process.py\", line 249, in _bootstrap\n",
        "    self.run()\n",
        "  File \"<ipython-input-48-076615bae24b>\", line 52, in run\n",
        "    self.tack.putUrl(url)\n",
        "AttributeError: 'WebPage' object has no attribute 'tack'\n"
       ]
      }
     ],
     "prompt_number": 49
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "regex = re.compile('https?:\\/\\/[a-z]+?\\.sohu.com\\/.*\\.s?html')\n",
      "url = 'fdsfs'\n",
      "match = regex.match(url)\n",
      "if not match:\n",
      "    print('yes')"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "yes\n"
       ]
      }
     ],
     "prompt_number": 47
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import IPython.nbformat.current as nbf\n",
      "\n",
      "nb = nbf.read(open('Untitled.ipynb', 'r'),'ipynb')\n",
      "\n",
      "nbf.write(nb,open('sina.py', 'w'), 'py')"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "metadata": {},
       "output_type": "pyout",
       "prompt_number": 57,
       "text": [
        "15051"
       ]
      }
     ],
     "prompt_number": 57
    }
   ],
   "metadata": {}
  }
 ]
}