import nltk
from urllib  import urlopen
import urlparse
from bs4 import BeautifulSoup
import unicodedata
import httplib

FILEIN = "weburls.txt"

FILEOUT = "bagofwords.txt"

TOPICS = ["Politics","Science","Arts","Sports","Business"]


def parseHTML(fullurl):


    o = urlparse.urlparse(fullurl)
        
    SERVER = o.netloc

    weburl = o.path
    
    connection = httplib.HTTPConnection(SERVER)
    connection.connect()
    connection.putrequest('GET', weburl)
    connection.putheader('Cookie','NYT-S=0MrwnLER.2CRfDXrmvxADeHJFXeaWHT8HPdeFz9JchiAJK89nlVaR7bsV.Ynx4rkFI; path=/; domain=.nytimes.com')
    connection.endheaders()
    response = connection.getresponse()
    html = response.read()
    #soup=BeautifulSoup(html)
    #main_div = soup.findALL(text=True)
    #raw = main_div.text
    #raw = unicodedata.normalize('NFKD', raw).encode('ascii','ignore')
    raw=nltk.clean_html(html)
    tokens = nltk.word_tokenize(raw)
    
    return tokens

def main():

    f=open(FILEIN)
    new = []

    for topic in TOPICS:
        new.append(open(topic+'words.txt','w'))

    for i in xrange(len(TOPICS)):
        for _ in range(100):
            words = []
            weburl = f.readline().strip()
            words = parseHTML(weburl)
            for word in words:
                new[i].write(word+' ')
            new[i].write('\n')

            
main()
