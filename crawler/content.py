#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import re
from HTMLParser import HTMLParser  
from re import sub  
from sys import stderr  
from traceback import print_exc  
 
from logger import logger
  
class _DeHTMLParser(HTMLParser):  
    def __init__(self):  
        HTMLParser.__init__(self)  
        self.__text = []  
  
    def handle_data(self, data):  
        text = data.strip()  
        if len(text) > 0:  
            text = sub('[ \t\r\n]+', ' ', text)  
            self.__text.append(text + ' ')  
  
    def handle_starttag(self, tag, attrs):  
        if tag == 'p':  
            self.__text.append('\n\n')  
        elif tag == 'br':  
            self.__text.append('\n')  
  
    def handle_startendtag(self, tag, attrs):  
        if tag == 'br':  
            self.__text.append('\n\n')  
  
    def text(self):  
        return ''.join(self.__text).strip()  
  
def dehtml(text):  
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:  
        parser = _DeHTMLParser()  
        parser.feed(text)  
        parser.close()  
        return parser.text()  
    except:  
        print_exc(file=stderr)  
        logger.error(text)
        return text  
  
def main(cont):  
    clear = re.compile('<SCRIPT[\s\S]*?</SCRIPT>',re.I)
    cont = clear.sub("",cont)
    clear = re.compile('<Style[\s\S]*?</Style>',re.I)
    cont = clear.sub("",cont)
    cont = dehtml(cont)
    return cont
  
if __name__ == '__main__':  
    with open('index.html','r') as fp:
        cont=fp.read()
    with open('index.txt','w') as fp:
        cont=fp.write(main(cont))
