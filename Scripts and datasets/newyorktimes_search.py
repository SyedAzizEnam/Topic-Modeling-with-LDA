import ast
import httplib
import time
import json

SERVER = 'api.nytimes.com'

OUTURLFILE = "weburls.txt"

OUTLABELSFILE = "weblabels.txt"

TOPICS = ["Politics","Science","Arts","Sports","Business"]

def SearchAndGet(query):
  
  url = '/svc/search/v2/articlesearch.json?' + query
  connection = httplib.HTTPSConnection(SERVER)
  connection.connect()
  connection.putrequest('GET', url)
  connection.endheaders()
  response = connection.getresponse()
  result_json = response.read()
  #print result_json
  decoder = json.JSONDecoder()
  result_dict = decoder.decode(result_json)
  return result_dict




def main():
  f1 = open(OUTURLFILE, 'w')
  f2 = open(OUTLABELSFILE,'w')
  for topic in TOPICS:
    for i in [0,2,3,4,5,6,7,8,9,10]:
      query= 'fq=news_desk:("' +topic+ '")%20AND%20document_type:("article")%20AND%20source:("The%20New%20York%20Times")&word_count>100&page=' +str(i)+ '&api-key=83994bf8975d2000bb753a592cda369a:0:68856824'
      #query = 'fq=news_desk:("'+topic+'")&facet_field=document_type&page='+str(i)+'&api-key=83994bf8975d2000bb753a592cda369a:0:68856824'  # There should be a url escaper library which you can use to convert whitespace to %20 etc. you could use that.
      print query
      result_dict = SearchAndGet(query)
      for doc in result_dict[u'response'][u'docs']:
        f1.write(str(doc[u'web_url']) + '\n')
        f2.write(topic+'\n')

  f1.close()
  f2.close()

main()
