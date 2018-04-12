#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

lanclass = {}
with open('crawler/parameter.conf', 'r') as fp:
    output = fp.readlines()
for lancla in output:
    one = lancla.strip().split('#')[0].split('=')
    if len(one)==2 and one[0] and one[1]:
        if one[1] in lanclass:
            lanclass[one[1].strip()] += [one[0].strip()]
        else:                                          
            lanclass[one[1].strip()] = [one[0].strip()]
lanclass = [(v,k) for k, v in lanclass.items()]
