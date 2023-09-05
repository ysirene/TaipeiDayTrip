import json
import mysql.connector
import os
from dotenv import load_dotenv
import re

with open('taipei-attractions.json', mode = 'r', encoding = 'utf-8') as file:
    data = json.load(file)
mrt_id = {}
mrt_num = 1
category_id = {}
category_num = 1

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
    elif attraction['MRT'] not in mrt_id:
        mrt_id[attraction['MRT']] = mrt_num
        mrt_num += 1
    if attraction['CAT'] not in category_id:
        category_id[attraction['CAT']] = category_num
        category_num += 1
    try:
        sight_data = (
            attraction['_id'],
            attraction['name'],
            category_id[attraction['CAT']],
            attraction['description'],
            attraction['address'],
            attraction['direction'],
            mrt_id[attraction['MRT']],
            attraction['latitude'],
            attraction['longitude'],
        )
    except:
        sight_data = (
            attraction['_id'],
            attraction['name'],
            category_id[attraction['CAT']],
            attraction['description'],
            attraction['address'],
            attraction['direction'],
            None,
            attraction['latitude'],
            attraction['longitude'],
        )
    cursor.execute('INSERT INTO sight(id, name, category_id, description, address, transport, mrt_id, lat, lng) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', sight_data)
    conn.commit()

    urls = attraction['file'].split('http')
    for url in urls:
        if re.match('.+\.jpg', url) or re.match('.+\.JPG', url):
            image_data = (attraction['_id'], 'http' + url)
            cursor.execute('INSERT INTO image(sight_id, url) VALUES(%s, %s);', image_data)
            conn.commit()

for station in mrt_id:
    mrt_data = (mrt_id[station], station)
    cursor.execute('INSERT INTO mrt(id, station) VALUES(%s, %s);', mrt_data)
    conn.commit()

for category in category_id:
    category_data = (category_id[category], category)
    cursor.execute('INSERT INTO category(id, cat) VALUES(%s, %s);', category_data)
    conn.commit()

cursor.close()
conn.close()