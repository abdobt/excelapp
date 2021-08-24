import json
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import numpy as np
from flask import request
def checkdataexistence(s,li):
   k=0
   found=0
   for e in li:
    k=k+1
    if s in e:
     return str(li[k - 1+9]).split()
   if (found == 0):
    return 0
def getdata(index,dt = []):
 arr=[]
 names = [
  'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
  'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE',
  'MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE',
  'BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE',
  'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE',
  'EURO FX - CHICAGO MERCANTILE EXCHANGE',
  'NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE',
  'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE',
  'U.S. DOLLAR INDEX - ICE FUTURES U.S',
  'SILVER - COMMODITY EXCHANGE INC',
  'GOLD - COMMODITY EXCHANGE INC'
 ]
 if(index=='1'):
  for d in dt:
   URL = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20"+d[4:6]+"/futures/deacmesf" + d + ".htm"
   page = requests.get(URL);
   soup = BeautifulSoup(page.content, "html.parser")
   li = soup.prettify().split('\n')
   for o in np.arange(0,8):
    a=checkdataexistence(names[o],li)
    if a==0:
      arr.append(['empty','empty','empty','empty','empty','empty','empty','empty','empty'])
    else:
      arr.append(a)
 elif(index=='2'):
  for d in dt:
   URL = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20"+d[4:6]+"/futures/deanybtsf"+d+".htm"
   page = requests.get(URL)
   soup = BeautifulSoup(page.content, "html.parser")
   li = soup.prettify().split('\n')
   a = checkdataexistence(names[8], li)
   if a == 0:
    arr.append(['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'])
   else:
    arr.append(a)
 else:
   for d in dt:
    URL = "https://www.cftc.gov/sites/default/files/files/dea/cotarchives/20"+d[4:6]+"/futures/deacmxsf" + d + ".htm"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    li = soup.prettify().split('\n')
    for o in np.arange(0, 2):
     a = checkdataexistence(names[o+9], li)
     if a == 0:
      arr.append(['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'])
     else:
      arr.append(a)
 return json.dumps(arr)
#il faut ajouter dix aux nombre de ligne souhaité
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/getdata', methods=['POST'])
@cross_origin(origin='*')
def home():
    return getdata(request.json['index'],request.json['dt'])