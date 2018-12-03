# __author__ = "Innocent Obi, edits by Jackie Cohen"

from media_library import *
from get_cache_itunes_data import *
import psycopg2, psycopg2.extras
import sys # for exit program mgmt
import json

# Set up lists for later (for instances)
media_list, song_list, movie_list = [], [], []
# Gather some sample data
media_samples = sample_get_cache_itunes_data("holiday")["results"]
song_samples = sample_get_cache_itunes_data("holiday", "music")["results"]
movie_samples = sample_get_cache_itunes_data("holiday", "movie")["results"]


# Now let's do some stuff with that data

# Modify empty lists from above
def createMediaList(media_samples, media_list):
    for item in media_samples:
        media = Media(item)
        media_list.append(media)

def createSongList(song_samples, song_list):
    for item in song_samples:
        song = Song(item)
        song_list.append(song)

def createMovieList(movie_samples, movie_list):
    for item in movie_samples:
        movie = Movie(item)
        movie_list.append(movie)

## Invoke each:
createMediaList(media_samples,media_list)
createSongList(song_samples, song_list)
createMovieList(movie_samples, movie_list)


### Set up database
try:
    conn = psycopg2.connect("dbname='media_508' user='jczetta'")
    print("Success connecting to database")
except:
    print("Unable to connect to the database. Check server and credentials.")
    sys.exit(1)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# For...
test_media_inst = media_list[0]
test_song_inst = song_list[0]
test_movie_inst = movie_list[0]
inst_list = [test_media_inst,test_song_inst,test_movie_inst]
# Invoke method on each
[inst.table_rep() for inst in inst_list]
all_insts = media_list + song_list + movie_list # flat list

## Now, for debugging, before writing the rest, may help to check out these keys, & comment these out after this part is done (printing is annoying & slow):
# print(test_media_inst.author_rep().keys())
# print(test_song_inst.author_rep().keys())
# print(sorted(list(test_media_inst.rep_diction.keys())), len(list(test_media_inst.rep_diction.keys())), "MEDIA KEYS")
# print(sorted(list(test_song_inst.rep_diction.keys())), len(list(test_song_inst.rep_diction.keys())),"SONG KEYS")
# print(sorted(list(test_movie_inst.rep_diction.keys())),len(list(test_movie_inst.rep_diction.keys())), "MOVIE KEYS")

# Note to self (or readers):
## If there's a problem with table structure, MAY be easier to drop table and recreate it differently, unless it's a lot of work to / impossible to recover the data (which shouldn't be the case for st like this)

## CREATE TABLE(S) IN DATABASE
cur.execute("CREATE TABLE IF NOT EXISTS Artists(name VARCHAR(500) PRIMARY KEY, primary_genre VARCHAR(250))") # To hold each name & primary genre info

cur.execute("CREATE TABLE IF NOT EXISTS Media({} VARCHAR(400),{} VARCHAR(400) PRIMARY KEY, {} VARCHAR(400), Artist_Name VARCHAR(500) REFERENCES Artists(name))".format(*sorted(list(test_media_inst.rep_diction.keys()))))

cur.execute("CREATE TABLE IF NOT EXISTS Song({} VARCHAR(400), {} VARCHAR(400), {} VARCHAR(400), {} VARCHAR(400) PRIMARY KEY, {} INTEGER, {} VARCHAR(400), {} VARCHAR(400), Artist_Name VARCHAR(500) REFERENCES Artists(name)) ".format(*sorted(list(test_song_inst.rep_diction.keys()))))

cur.execute("CREATE TABLE IF NOT EXISTS Movie({} TEXT, {} VARCHAR(400),{} VARCHAR(400), {} VARCHAR(400) PRIMARY KEY, {} INTEGER, {} VARCHAR(400), {} VARCHAR(400), {} INTEGER, Artist_Name VARCHAR(500) REFERENCES Artists(name))".format(*sorted(list(test_movie_inst.rep_diction.keys()))))

conn.commit()

## Insert data into tables

# First, insert all artists from each list into artist table by invoking artist rep method on media &c class, handling duplicates -- see draft stmt below
artistdictions = [x.author_rep() for x in all_insts]
cur.executemany("INSERT INTO Artists(name, primary_genre) VALUES (%(name)s, %(primary_genre)s) ON CONFLICT DO NOTHING",artistdictions)
conn.commit()
#cur.executemany("""INSERT INTO Songs(Title,Artist,Num_Plays) VALUES (%(Title)s, %(Artist)s, %(Num_Plays)s)""",songsdictions)


# stmt: INSERT INTO table_name(column_list) VALUES(value_list) ON CONFLICT DO NOTHING; # don't want to update if the artist is already there, it's already there, cool [but note that ANY difference is... still a difference]

# Insert Media data into media table, referencing artists
# First, create a list of media dictionaries that will hold both the movie information and the artist name information to ref. the other table and build a relationship -- this process, with careful changing of variables, can be repeated for other types.
# There are of course many ways to organize this -- but easier implementation often requires more complexity at the get-go; it can be best to strike a balance.
mediadictions = []
for inst in media_list:
    diction = inst.table_rep()
    diction["artist_name"] = inst.author
    mediadictions.append(diction)
sql = "INSERT INTO Media({},{}, {})".format(*sorted(list(test_media_inst.table_rep().keys()))) + " VALUES (%({})s, %({})s, %({})s) ON CONFLICT DO NOTHING".format(*sorted(list(test_media_inst.table_rep().keys())))
cur.executemany(sql,mediadictions)
conn.commit()

# Insert Song data into media table, referencing artists
# First, create a list of song dictionaries that will hold both the movie information and the artist name information to ref. the other table and build a relationship
songdictions = []
for inst in song_list:
    diction = inst.table_rep()
    diction["artist_name"] = inst.author
    songdictions.append(diction)
sql = "INSERT INTO Song({},{}, {},{},{},{},{},artist_name)".format(*sorted(list(test_song_inst.table_rep().keys()))) + " VALUES (%({})s, %({})s, %({})s, %({})s, %({})s, %({})s, %({})s, %(artist_name)s) ON CONFLICT DO NOTHING".format(*sorted(list(test_song_inst.table_rep().keys())))
cur.executemany(sql,songdictions)
conn.commit()

# Insert Movie data into media table, referencing artists
# First, create a list of movie dictionaries that will hold both the movie information and the artist name information to ref. the other table and build a relationship


# TODO: do the same for the movie table


# Create additional searches and enter them into tables

# You'll want a new file for making queries



### AND DONE
conn.close()
