import json
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import numpy as np
from flask import request
def getdata(index,dt = []):
 arr=[]
 if(index=='1'):
  print("hello")
  for d in dt:
   print("hello dt")
   URL = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20"+d[4:6]+"/futures/deacmesf" + d + ".htm"
   page = requests.get(URL);
   soup = BeautifulSoup(page.content, "html.parser")
   li = soup.prettify().split('\n')
   i=0
   for d in li:
    i=i+1
    if 'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE' in d:
     print(str(li[i-1]))
     break
   for a in np.arange(0,6):
    arr.append(str(li[(i - 1+9)+(21*a)]).split())
   arr.append(str(li[i - 1 +198]).split())
   k=0
   for e in li:
    k=k+1
    if 'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE' in e:
     arr.append(str(li[k - 1+9]).split())
     break
 elif(index=='2'):
  for d in dt:
   URL = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20"+d[4:6]+"/futures/deanybtsf"+d+".htm"
   page = requests.get(URL)
   soup = BeautifulSoup(page.content, "html.parser")
   li = soup.prettify().split('\n')
   k=0
   for e in li:
    k=k+1
    if 'U.S. DOLLAR INDEX - IC E FUTURES U.S' in e:
     arr.append(str(li[k - 1+9]).split())
     break
 else:
   for d in dt:
    URL = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20"+d[4:6]+"/futures/deacmxsf" + d + ".htm"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    li = soup.prettify().split('\n')
    k = 0
    for e in li:
     k = k + 1
     if ('SILVER - COMMODITY EXCHANGE INC' in e) or ('GOLD - COMMODITY EXCHANGE INC.' in e):
      arr.append(str(li[k - 1 + 9]).split())
 return json.dumps(arr)
#il faut ajouter dix aux nombre de ligne souhaité
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/getdata', methods=['POST'])
@cross_origin(origin='*')
def home():
    return getdata(request.json['index'],request.json['dt'])
app.run(port=5000)