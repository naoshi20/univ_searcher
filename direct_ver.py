import re
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3

#Connecting to the file in which we want to store our db
conn = sqlite3.connect('direct_ver.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Univ
    ( deviation INTEGER, univ TEXT, department TEXT, distance INTEGER, time INTEGER)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# enter your API key
api_key = 'AI***__________'
serviceurl = 'https://maps.googleapis.com/maps/api/directions/json?'

filepath1 = 'univ_deviation.htm'
with open(filepath1 , encoding='utf-8') as f1:
    html1 = f1.read()
soup1 = BeautifulSoup(html1, 'html.parser')
trs1 = soup1.select("tr")

parms = dict()
parms['origin'] = input('住所を入力してください：')
parms['key'] = api_key

for tr in trs1[83:41]:
    ps = tr.select('p') #list-type
    lilist = tr.select('tr td ul li ul li')
    for ptag in ps:
        try:
            dev = ptag.getText('p')
            dev = int(dev)
        except:
            dev = '?'
        for li in lilist:
            try:
                x = li.getText('li')
                xlist = x.split('li')
                y = xlist[0] + '学'
                z = xlist[1][1:-1] + '学部'
                parms['destination'] = y + ' ' + z
                url = serviceurl + urllib.parse.urlencode(parms)
                uh = urllib.request.urlopen(url, context=ctx)
                data = uh.read().decode()
                try:
                    js = json.loads(data)
                except:
                    js = None
                try:
                    distance = js['routes'][0]['legs'][0]['distance']['value']
                    distance = round(distance / 1000, 1)
                    time = js['routes'][0]['legs'][0]['duration']['value']
                    time = round(time / 60)
                except:
                    print(json_error)
            except:
                y = '?'
                z = '?'
                distance ='?'
                time = '?'
            cur.execute('''INSERT OR IGNORE INTO Univ (deviation, univ, department, distance, time)
                    VALUES ( ?, ?, ?, ?, ? )''', ( dev, y, z, distance, time ) )
            print(next)
conn.commit()

# Getting the top 10 results and showing them
sql = 'SELECT deviation, univ, department, distance, time FROM Univ ORDER BY deviation DESC LIMIT 5'
print("Counts:")
for row in cur.execute(sql) :
    print(row[0], row[1])

#Closing the DB
cur.close()
