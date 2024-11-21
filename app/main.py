import os
import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
baseurl = 'http://dqb5ee-dp1-spotify.s3-website-us-east-1.amazonaws.com/'

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "dqb5ee"

@app.get('/genres')
def get_genres():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        cur.close()
        db.close()

@app.route('/songs', methods=['GET'])
def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = """
        SELECT
            songs.title,
            songs.album,
            songs.artist,
            songs.year,
            songs.file AS mp3_file,
            songs.image AS jpg_file,
            genres.genre AS genre
        FROM songs
        JOIN genres ON songs.genre = genres.genreid
        ORDER BY songs.title;
    """
    try:
        cur.execute(query)
        results = cur.fetchall()

        songs = [
            {
                "title": row[0],
                "album": row[1],
                "artist": row[2],
                "year": row[3],
                "mp3_file": baseurl + row[4],  # Full S3 URL for mp3 file
                "jpg_file": baseurl + row[5],  # Full S3 URL for image file
                "genre": row[6]
            }
            for row in results
        ]

        # Return the songs as a JSON response
        return json.dumps(songs)
    except Error as e:
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}
    finally: 
        cur.close()
        db.close()
