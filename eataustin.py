import urllib.request as request
import json

response=request.urlopen('https://data.austintexas.gov/api/views/ecmv-9xxi/rows.json?accessType=DOWNLOAD')
data=response.read()
encoding=response.info().get_content_charset()
austin=json.loads(data.decode(encoding))
meta=austin['meta']['view']

keys=meta.keys()
keys_pos=[]
for i in keys:
    if type(meta[i]) == dict:keys_pos.append(i)
    if type(meta[i]) == list:keys_pos.append(i)


austin_data=austin['data']
aust={}
for i in range(len(austin_data)):
    aust[austin_data[i][8]]=austin_data[i]

keys=aust.keys()
scores={}
for i in keys:
    scores[i]={}
    scores[i]['Address']=aust[i][12]
    scores[i]['Score']=aust[i][11]
    scores[i]['Zip']=aust[i][9]
    street=scores[i]['Address'][0].split("\"")[3]
    street=street.replace(" ","+")
    city=scores[i]['Address'][0].split("\"")[7]
    state=scores[i]['Address'][0].split("\"")[11]
    location="{}+{}+{}+{}".format(street,city,state,scores[i]['Zip'])
    location=location.replace(" ","+")
    url='https://www.google.com/maps/place/'+location
    scores[i]['Map']=url

def getScoreList(min=0,max=100):
    final_list=[]
    for i in scores.keys():
        score=int(scores[i]['Score'])
        if (score > min) & (score < max):final_list.append(i)
    return final_list

def displayData(restaraunt_list):
    for i in restaraunt_list:
        print(i+': '+ scores[i]['Score'])
        print(scores[i]['Map']+'\n')


