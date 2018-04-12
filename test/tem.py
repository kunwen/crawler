import urllib  
import urllib2  
import os, re  
from BeautifulSoup import BeautifulSoup  
  
URL = "https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes"  
page = urllib2.urlopen(URL)  
soup = BeautifulSoup(page)  
page.close()  
  
tables = soup.findAll('table')  
tab = tables[1]  
x = {}
for tr in tab.findAll('tr'):  
    #for td in tr.findAll('td'):  
    #    print td.getText(),  
    td = tr.findAll('td')
    if len(td)>4:
        x[td[4].getText()] = td[2].getText()+'  '+ td[3].getText()+ '  '+ td[1].getText()
print x
