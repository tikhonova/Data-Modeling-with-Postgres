# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE table IF NOT EXISTS songplays (
    songplay_id serial primary key,
    start_time timestamp NOT NULL, 
    user_id int NOT NULL,
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id int, 
    location varchar, 
    user_agent varchar NOT NULL
)""")

user_table_create = ("""
CREATE table IF NOT EXISTS users (
    user_id varchar primary key, 
    first_name varchar NOT NULL,
    last_name varchar NOT NULL, 
    gender varchar, 
    level varchar NOT NULL
 )""")

song_table_create = ("""
CREATE table IF NOT EXISTS songs (
    song_id varchar primary key, 
    title varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    year int, 
    duration numeric NOT NULL
)""")

artist_table_create = ("""
CREATE table IF NOT EXISTS artists (
    artist_id varchar primary key, 
    name varchar NOT NULL, 
    location varchar, 
    latitude decimal, 
    longitude decimal
)""")

time_table_create = ("""
CREATE table IF NOT EXISTS time (
    start_time timestamp primary key, 
    hour int NOT NULL, 
    day int NOT NULL, 
    week int NOT NULL, 
    month int NOT NULL, 
    year int NOT NULL, 
    weekday varchar NOT NULL
)""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT into songplays (
    start_time, 
    user_id, 
    level, 
    song_id, 
    artist_id, 
    session_id, 
    location, 
    user_agent)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""")

user_table_insert = ("""
INSERT into users (
user_id, 
first_name,
last_name,
gender,level)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (user_id) DO UPDATE 
SET level = excluded.level;
""")

song_table_insert = ("""
INSERT into songs (
song_id, 
title, 
artist_id, 
year, 
duration)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
INSERT into artists (
artist_id, 
name, 
location, 
latitude, 
longitude)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = ("""
INSERT into time (
start_time, 
hour, 
day, 
week, 
month, 
year, 
weekday)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT songs.song_id, artists.artist_id 
FROM songs 
JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s 
    AND artists.name = %s 
    AND songs.duration = %s;
""")

#("""SELECT s.song_id, s.artist_id, s.title as song,
#a.name as artist, s.duration as length
#FROM songs s
#JOIN artists a on a.artist_id = s.artist_id
#""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]