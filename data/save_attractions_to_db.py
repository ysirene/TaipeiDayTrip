import json
import mysql.connector
import os
from dotenv import load_dotenv
import re

with open('taipei-attractions.json', mode = 'r', encoding = 'utf-8') as file:
    data = json.load(file)
station_id = {}
num = 1

load_dotenv()
conn = mysql.connector.connect(
    host = 'localhost',
    database = 'tripweb',
    user = os.getenv('user'),
    password = os.getenv('password')
)
cursor = conn.cursor()
for i in range(len(data['result']['results'])):
    attraction = data['result']['results'][i]
    if attraction['MRT'] == None:
        pass
    elif attraction['MRT'] not in station_id:
        station_id[attraction['MRT']] = num
        num += 1
    urls = attraction['file'].split('http')
    image_data = []
    for url in urls:
        if re.match('.+\.jpg', url) or re.match('.+\.JPG', url):
            image_data.append('http' + url)
    try:
        sight_data = (
            attraction['_id'],
            attraction['name'],
            attraction['CAT'],
            attraction['description'],
            attraction['address'],
            attraction['direction'],
            station_id[attraction['MRT']],
            attraction['latitude'],
            attraction['longitude'],
            ','.join(image_data)
        )
    except:
        sight_data = (
            attraction['_id'],
            attraction['name'],
            attraction['CAT'],
            attraction['description'],
            attraction['address'],
            attraction['direction'],
            None,
            attraction['latitude'],
            attraction['longitude'],
            ','.join(image_data)
        )
    cursor.execute('INSERT INTO sight(id, name, category, description, address, transport, mrt_id, lat, lng, images) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', sight_data)
    conn.commit()
for station in station_id:
    mrt_data = (station_id[station], station)
    cursor.execute('INSERT INTO mrt(id, station) VALUES(%s, %s);', mrt_data)
    conn.commit()

cursor.close()
conn.close()