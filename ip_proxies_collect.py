'''
@author: xiaoye
'''
import requests
from bs4 import BeautifulSoup as bs
import re
import Queue
import threading

url = 'http://www.xicidaili.com/nn/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

class Ip_collect(threading.Thread):
    
    def __init__(self, que):
        threading.Thread.__init__(self)
        self._que = que
    
    def run(self):
        while not self._que.empty():
            url = self._que.get()
            r = requests.get(url, headers=headers, timeout=6)
            #print r.content, r.status_code
            soup = bs(r.content, 'lxml', from_encoding='utf-8')
            bqs = soup.find_all(name='tr', attrs={'class':re.compile(r'|[^odd]')})
            for bq in bqs:
                #print bq
                us = bq.find_all(name='td')
                #print us[1].string
                #print str(us[1].string), str(us[2].string), str(us[5].string)
                try:
                    self.ip_proxies_confirm(str(us[5].string), str(us[1].string), str(us[2].string))
                except Exception,e:
                    print e
                    pass
    
    def ip_proxies_confirm(self, type_self, ip, port):
        ip_dic = {}
        ip_dic[type_self.lower()] = ip + ':' + port
        print ip_dic
        r = requests.get('http://1212.ip138.com/ic.asp', headers=headers, proxies=ip_dic, timeout=6)
        result = re.findall(r'\d+\.\d+\.\d+\.\d+', r.content)
        result_ip = ''.join(result)
        print result_ip
        if ip == result_ip:
            print ip + ':' + port + ' is ok!!\n'
            with open('ips.txt', 'a') as f:
                f.write(ip + ':' + port + '\n')
    
#ip_proxies_spider()
if __name__ == '__main__':
    thread = []
    thread_count = 16
    que = Queue.Queue()
    for i in range(1, 10):
        que.put('http://www.xicidaili.com/nn/' + str(i))
    
    for i in range(thread_count):
        thread.append(Ip_collect(que))
    for i in thread:
        i.start()
    for i in thread:
        i.join()

