#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import re, langid, chardet, codecs

from crawler.logger import logger
from crawler.parameter import *
from crawler.check import *

'''{'24': 'fa', '25': 'fi', '26': 'fo', '27': 'fr', '20': 'eo', '21': 'es', '22': 'et', '23': 'eu', '28': 'ga', '29': 'gl', '4': 'ar', '8': 'bg', '59': 'ms', '58': 'mr', '55': 'mk', '54': 'mg', '57': 'mn', '56': 'ml', '51': 'lo', '50': 'lb', '53': 'lv', '52': 'lt', '88': 'tr', '89': 'ug', '82': 'sv', '83': 'sw', '80': 'sq', '81': 'sr', '86': 'th', '87': 'tl', '84': 'ta', '85': 'te', '3': 'an', '7': 'be', '39': 'it', '38': 'is', '33': 'hr', '32': 'hi', '31': 'he', '30': 'gu', '37': 'id', '36': 'hy', '35': 'hu', '34': 'ht', '60': 'mt', '61': 'nb', '62': 'ne', '63': 'nl', '64': 'nn', '65': 'no', '66': 'oc', '67': 'or', '68': 'pa', '69': 'pl', '2': 'am', '6': 'az', '91': 'ur', '90': 'uk', '93': 'vo', '92': 'vi', '95': 'xh', '94': 'wa', '97': 'zu', '96': 'zh', '11': 'bs', '10': 'br', '13': 'cs', '12': 'ca', '15': 'da', '14': 'cy', '17': 'dz', '16': 'de', '19': 'en', '18': 'el', '48': 'ky', '49': 'la', '46': 'ko', '47': 'ku', '44': 'km', '45': 'kn', '42': 'ka', '43': 'kk', '40': 'ja', '41': 'jv', '1': 'af', '5': 'as', '9': 'bn', '77': 'si', '76': 'se', '75': 'rw', '74': 'ru', '73': 'ro', '72': 'qu', '71': 'pt', '70': 'ps', '79': 'sl', '78': 'sk'}   
'''
class LangagesofFamily(object):
    def __init__(self):
        self.lanclass = lanclass 
        self.countrylist = ','.join([','.join(i[1]) for i in self.lanclass]).split(',')
  
    def translate(self, inputFile, outputFile, lik, ssize):
        try:
            fin = inputFile.decode('utf-8')
        except Exception:
            pass
        lineTuple = langid.classify(inputFile)                     #调用langid来对该行进行语言检测
        if lineTuple[0] in lik[0]:
            p = re.compile(r'[\n]+')
            with codecs.open(outputFile, 'w', "utf-8") as fout:          #以写的方式打开输出文件
                try:
                    fout.writelines(p.sub('\n', inputFile))
                except Exception:
                    fout.writelines(p.sub('\n', fin))
            return True
        else:
            return False

if __name__ == '__main__':                                            #相当于main函数  
    langages = LangagesofFamily()
    print (langages.lanclass)
    lik = raw_input("请输入一个圆括号的内容，如：\"(['zh'] ,'Chinese_Simp')\" >>>")  
    lik = eval(lik)
    fin = open('index.txt', 'r').read()                           #以读的方式打开输入文件  
    langages.translate(fin, "myOutputFile.txt", lik, 500)
