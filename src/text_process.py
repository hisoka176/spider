#encoding=utf-8
import sys
from imp import reload
reload(sys)
import pymysql
import datetime
import time
import re
re.compile('活动时间')

db = pymysql.connect(host="localhost",user="root",passwd="root",db="hisoka_test",charset="utf8")
 
cursor = db.cursor()
 
cursor.execute('SET NAMES utf8;') 
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

class OutPut(object):
    def __init__(self):
        self.db = self.connect(host="localhost",user="root",passwd="root",charset="utf8")
        self.cursor = self.cursor()
        cursor.execute('SET NAMES utf8;') 
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        # create table
        sql = '''create table if not exists active
            (
            sdate datetime,
            edate datetime,
            active string
            )'''
        try:
            cursor.execute(sql)
            db.commit()
        except:
            pass
    
    def output(self,sdate,edate,active):
        pass
class Process(object):
    def __init__(self,url,title,publish_data,start_time,end_time,content):
        self.url,self.title,self.publish_data,self.start_time,self.end_time,self.content = url,title,publish_data,start_time,end_time,content
        self.regex = re.compile("活动时间")
        self.content = self.content.replace("：",":")
        self.regexD = re.compile('([\d]{4})年([\d]{1,2})月([\d]{1,2})日([\d]{1,2}):([\d]{1,2})')
        
    def processDate(self,dString,mark=True):
        
        def double_bit(string):
            if len(string)==1:
                return '0%s' % string
            else:
                return string
            
        dString = dString.replace(' ','')
        dString = dString.strip()
        
        
        year = re.match('([\d]{4})年',dString)
        month = re.match('.*?([\d]{1,2})月',dString)
        day = re.match('.*?([\d]{1,2})日',dString)
        
        if year:
            year = double_bit(year.group(1))
        else:
            year = datetime.datetime.strptime(self.publish_data,'%Y-%m-%d %H:%M:%S').year
        if month:
            month = double_bit(month.group(1))
        if day:
            day = double_bit(day.group(1))
        
        if "新版本" in dString: 
            
            datestamp = datetime.datetime.strptime(self.publish_data,'%Y-%m-%d %H:%M:%S')  
            year = datestamp.year
            month = double_bit(str(datestamp.month))
            day = double_bit(str(datestamp.day))    
        
       
        return '%s-%s-%s' % (year,month,day)
  
        
        
    def getType(self):
        texts = self.content.split('\t')
        type = ''
        if "消费返利" in self.title:
            type = "消费返利"
        if "充值返利" in self.title:
            type = "充值返利"
        if "消返" in self.title:
            type = "消费返利"
        if "充返" in self.title:
            type = "充值返利"
        if "充值" in self.title:
            type = "充值返利"
        if "消费" in self.title:
            type = "消费返利"
            
        for i in texts:
            if "充值" in i:
                type = "充值返利"
                break
            if "消费" in i:
                type = "消费返利"
                break
            if "消费返利" in i:
                type = "消费返利"
                break
            if "充值返利" in i:
                type = "充值返利"
                break
            if "消返" in i:
                type = "消费返利"
                break
            if "充返" in i:
                type = "充值返利"
                break
        if type=='':
            return (False,None)
        return (True,type)
    
    def getDate(self):
        
        texts = self.content.split('\t')
        sdate = ''
        edate = ''
        string = ''
        
        for i in texts:
            if "时间:" in i:
                string = i
        
        if string == '':
            return (False,sdate,edate)
        
        # process date
    
        index = string.index(':')
        string = string[index+1:]
        date_array = string.split("至")
        
        if len(date_array) == 2:
            sdate = date_array[0]
            edate = date_array[1]
            return (True,self.processDate(sdate,True),self.processDate(edate,False))
        
        elif len(date_array) != 2:
            if '开始' in string  and '结束' in string:
                string = string.replace('开始','\t') 
                string = string.replace('结束','\t')
                string_array = string.split('\t')
                string_array = [ i  for i in string_array if i != '' ]
                if len(date_array) == 2:
                    sdate = date_array[0]
                    edate = date_array[1]
                    return (True,self.processDate(sdate,True),self.processDate(edate,False))
                else:
                    return (False,sdate,edate)
            else:
                return (False,sdate,edate)
            
    def  process_text(self):
        amark,active_type = self.getType()
        mark,sdate,edate = self.getDate()
        string = ''
        if amark and mark:
            string = sdate,edate,active_type
            if sdate=='' and edate =='':
                string = amark,mark,self.content.split('\t')
                string = [str(i) for i in string]
#             ##  看case用            
#              string = amark,mark,self.content.split('\t')
#              string = [str(i) for i in string]
        else:
            return string
        return ','.join(string)
            
    def __str__(self):
        string = self.process_text()   
        return string
        
        
         
      
            
def main():
    file = './recharge.txt'
    f = open(file,'a+',encoding='utf-8')
    sql = "select * from tlbb;"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        a = Process(*i)
        if str(a)=='':
            continue
        f.write('%s,1400140930701\n' % (a))
    f.close()
    
        
if __name__=='__main__':  
    main()
    
    

 