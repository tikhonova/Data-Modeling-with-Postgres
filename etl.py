import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Process and load data from song file
        Args:
            # cur: database cursor
            # filepath: path to song file"""
    # open song file
    df = pd.read_json(filepath, lines=True)

    for index, row in df.iterrows():
        # insert song record
        song_data = (row.song_id, row.title, row.artist_id,
                     row.year, row.duration)
        try:
            cur.execute(song_table_insert, song_data)
        except psycopg2.Error as error:
            print("Error: failure to insert song rows")
            print(error)

        # insert artist record
        artist_data = (row.artist_id, row.artist_name, row.artist_location,
                       row.artist_latitude, row.artist_longitude)
        try:
            cur.execute(artist_table_insert, artist_data)
        except psycopg2.Error as error:
            print("Error: failure to insert artist rows")
            print(error)


def process_log_file(cur, filepath):
    """Process and load data from log file
        Args:
            # cur: database cursor
            # filepath: path to log file"""
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    t = df.copy()

    # insert time data records
    timedata = (t.ts, t.ts.dt.hour, t.ts.dt.day,
                t.ts.dt.dayofweek, t.ts.dt.month,
                t.ts.dt.year, t.ts.dt.weekday)
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    timedf = pd.DataFrame(columns=column_labels)

    for index, column_label in enumerate(column_labels):
        timedf[column_label] = timedata[index]

    for i, row in timedf.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as error:
            print("Error: failure to insert time rows")
            print(error)

    # load user table
    user_df = df.filter(['userId', 'firstName', 'lastName',
                         'gender',
                         'level']).drop_duplicates('userId').dropna(subset=['userId'])

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as error:
            print("Error: failure to insert user rows")
            print(error)

    # insert songplay records

    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, int(row.userId),
                         row.level, songid, artistid, row.sessionId,
                         row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
       # cur.fetchone()


def process_data(cur, conn, filepath, func):
    """Process JSON files from filepath location
        Args:
        # cur: database cursor
        # conn: psycopg2 connection
        # filepath: filepath to song file
        # func: function for processing each file"""

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Create database connection,
    process song & logs information,
    close cursor & database connection
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
