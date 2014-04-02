import nltk
from urllib  import urlopen
import urlparse
from bs4 import BeautifulSoup
import unicodedata
import httplib


FILEIN = "weburls.txt"

FILEOUT = "bagofwords1.txt"


def getvocab():

    fvocab=open("vocab.txt","w")
    vocab = []
    
    TOPICS = ["Politics","Science","Arts","Sports","Business"]
    
    for topic in TOPICS:
        f=open('TOP' +topic+ 'words.txt')
        while (f):
            word = f.readline().strip()

            if not word:
                break
            
            if word not in vocab:
                vocab.append(word)
                fvocab.write(word + '\n')
                
        f.close()

    return vocab


def parseHTML(fullurl):


    o = urlparse.urlparse(fullurl)
        
    SERVER = o.netloc

    weburl = o.path
    
    connection = httplib.HTTPConnection(SERVER)
    connection.connect()
    connection.putrequest('GET', weburl)
    connection.putheader('Cookie','RMID=007f01013427530f1d59000a; NYT-S=0MmHbUyeZD2mTDXrmvxADeHDzSyKJyJAlfdeFz9JchiAIUFL2BEX5FWcV.Ynx4rkFI')
    connection.endheaders()
    response = connection.getresponse()
    html = response.read()
    #soup=BeautifulSoup(html)
    #main_div = soup.findALL(text=True)
    #raw = main_div.text
    #raw = unicodedata.normalize('NFKD', raw).encode('ascii','ignore')
    raw=nltk.clean_html(html)
    tokens = nltk.word_tokenize(raw)
    if not tokens:
        print fullurl
    return tokens

def main():

    f=open(FILEIN)

    fout=open(FILEOUT,"w")

    vocab = getvocab()

    line = 0
    zero_count = 0
    while(f):

        zero_so_far = True
        bagofwords={w:0 for w in vocab}
        #for i in range(475):
        #    weburl = f.readline().strip()
        weburl = f.readline().strip()
        line +=1
        print line
        words = parseHTML(weburl)

        for word in words:
            word=word.strip().lower()
            if word=="olympics":
                print word
            if word in bagofwords.keys():
                bagofwords[word] +=1
                zero_so_far = False
            else:
                continue
            
        for key,val in bagofwords.items():
            fout.write(str(val)+' ')
        if zero_so_far:
            zero_count += 1
            print "zero)count%d" %zero_count

        
        fout.write('\n')

main()
