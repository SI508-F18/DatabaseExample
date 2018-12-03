import psycopg2, psycopg2.extras
import sys # for exit program mgmt
import json

try:
    conn = psycopg2.connect("dbname='media_508' user='jczetta'")
    print("Success connecting to database")
except:
    print("Unable to connect to the database. Check server and credentials.")
    sys.exit(1)

## Make some type of queries, like...
cur.execute("select * from song where artist_name='Green Day'")
res = cur.fetchall()
print(res) # [['American Idiot', 'Alternative', 'https://itunes.apple.com/us/album/holiday/1161539183?i=1161539473&uo=4', '1161539473', 232, 'Holiday', '3', 'Green Day'], ['American Idiot (The Original Broadway Cast Recording)', 'Soundtrack', 'https://itunes.apple.com/us/album/holiday-feat-john-gallagher-jr-stark-sands-theo-stockman/366916135?i=366916211&uo=4', '366916211', 247, 'Holiday (feat. John Gallagher Jr., Stark Sands, Theo Stockman & Company)', '3', 'Green Day'], ["Greatest Hits: God's Favorite Band", 'Alternative', 'https://itunes.apple.com/us/album/holiday/1295796853?i=1295797525&uo=4', '1295797525', 232, 'Holiday', '13', 'Green Day']]

# Also, play around with psql for queries...
