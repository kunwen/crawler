#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import os
from crawler import *

#with open('index.html','r') as fp:
#    cont=fp.read()
#with open('index.txt','w') as fp:
#    cont=fp.write(content.main(cont))

#langages = lang.LangagesofFamily()
#print langages.lanclass
#lik = raw_input("请输入一个圆括号的内容，如：\"(['zh'] ,'Chinese_Simp')\" >>>")  
#lik = eval(lik)
#fin = open('index.txt', 'r').read()                           #以读的方式打开输入文件  
#langages.translate(fin, "myOutputFile.txt", lik, 500)

import codecs
from crawler import content, lang

if '__main__' == __name__:
    with codecs.open('index.html','r', "utf-8") as fp:
        cont=fp.read()
    with codecs.open('index.txt','w', "utf-8") as fp:
        cont=fp.write(content.main(cont))

    langages = lang.LangagesofFamily()
    print (langages.lanclass)
    lik = input("请输入一个圆括号的内容，如：\"(['zh'] ,'Chinese_Simp')\" >>>")  
    lik = eval(lik)
    fin = codecs.open('index.txt', 'r', "utf-8").read()                           #以读的方式打开输入文件
    try:
        langages.translate(fin, "myOutputFile.txt", lik, 500)
    except Exception as err:
        fin = fin.encode('utf-8')
        langages.translate(fin, "myOutputFile.txt", lik, 500)

#if '__main__' == __name__:
#    path = os.path.dirname(os.path.realpath(__file__))
#    try:
#        os.system(path + '/test_env/bin/python ' + path +'/crawler/content.pyc')
#        os.system(path + '/test_env/bin/python ' + path +'/crawler/lang.pyc')
#    except Exception as err:
#        print ('content.pyc文件或者lang.pyc文件缺失！')
