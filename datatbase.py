#############################################################
# This program will setup databaseb create all tables.      #
# Downloads  all the data from EONET API. And saves them to #
#  database. Then extracts the required data and saves it   #
# to data.csv file. In the end prints success after all the #
#  actions are completed                                    #
#############################################################

import sqlite3
import requests
import csv

conn = sqlite3.connect('EONET.db')
c = conn.cursor()

#Creates all the required tables
def table_events():
    c.execute('CREATE TABLE IF NOT EXISTS events(events_id TEXT, title TEXT, description TEXT, link TEXT, PRIMARY KEY (events_id))')

def table_categories():
    c.execute('CREATE TABLE IF NOT EXISTS categories(events_id TEXT, categories_id INT,title TEXT,PRIMARY KEY (events_id, categories_id))')

def table_sources():
    c.execute('CREATE TABLE IF NOT EXISTS sources(events_id TEXT,sources_id TEXT,url TEXT, PRIMARY KEY (events_id, sources_id))')

def table_geometries():
    c.execute('CREATE TABLE IF NOT EXISTS geometries(events_id TEXT, geometries_id TEXT, type TEXT, coordinates TEXT)')

#loads the data from api to the database
def load_db():
    url = "https://eonet.sci.gsfc.nasa.gov/api/v2.1/events"
    data = requests.get(url).json()
    for eve in range(0,len(data['events'])):
        c.execute("INSERT INTO events (events_id, title, description, link) VALUES (?, ?, ?, ?)",
                  (data['events'][eve]['id'], data['events'][eve]['title'], data['events'][eve]['description'], data['events'][eve]['link']))
        conn.commit()

        for cat in range(0,len(data['events'][eve]['categories'])):
            c.execute("INSERT INTO categories (events_id, categories_id, title) VALUES (?, ?, ?)",
                      (data['events'][eve]['id'], data['events'][eve]['categories'][cat]['id'], data['events'][eve]['categories'][cat]['title']))
            conn.commit()

        for geo in range(0,len(data['events'][eve]['geometries'])):
            c.execute("INSERT INTO geometries (events_id, geometries_id, type, coordinates) VALUES (?, ?, ?, ?)",
                      (data['events'][eve]['id'], data['events'][eve]['geometries'][geo]['date'], data['events'][eve]['geometries'][geo]['type'],str(data['events'][eve]['geometries'][geo]['coordinates'])))
            conn.commit()

        for sou in range(0,len(data['events'][eve]['sources'])):
            c.execute("INSERT INTO sources (events_id, sources_id, url) VALUES (?, ?, ?)",
                      (data['events'][eve]['id'], data['events'][eve]['sources'][sou]['id'], data['events'][eve]['sources'][sou]['url']))

    sql = '''
    select
    e.events_id, e.title, e.description, e.link,
    c.categories_id,c.title as categories_title,
    g.geometries_id, g.type, g.coordinates,
    s.sources_id, s.url
    from events e,categories c, geometries g, sources s
    where e.events_id = c.events_id and c.events_id = g.events_id and g.events_id = s.events_id
    and c.title in ('Wildfires', 'Severe Storms', 'landslides') and
     substr(geometries_id,1,4)||substr(geometries_id,6,2)||substr(geometries_id,9,2) between '20180501' and '20180531'
    '''

    result = c.execute(sql)
    writer = csv.writer(open("data.csv", 'w', newline=''))
    col = ['events_id', 'title', 'description', 'link', 'categories_id', 'categories_title', 'geometries_id', 'type',
           'coordinates', 'sources_id', 'url']
    writer.writerow(col)
    for row in result:
        writer.writerow(row)

    c.close()
    conn.close()
    print("success")

table_events()
table_categories()
table_sources()
table_geometries()
load_db()



