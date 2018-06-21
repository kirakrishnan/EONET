####################################################
# This program will clear the entire database      #
####################################################

import sqlite3

conn = sqlite3.connect('EONET.db')
c = conn.cursor()

c.execute("delete from sources")
c.execute("delete from events")
c.execute("delete from categories")
c.execute("delete from geometries ")
conn.commit()

c.close()
conn.close()

Print("Data removed from all the tables")