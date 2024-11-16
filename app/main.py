import os
import mysql.connector
from fastapi import FastAPI

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DBNAME = "dqb5ee"

try:
    db = mysql.connector.connect(
        user=DBUSER,
        host=DBHOST,
        password=DBPASS,
        database=DBNAME
    )
    cur = db.cursor()
    print("Database connection successful")
except mysql.connector.Error as err:
    print(f"Error: {err}")

@app.get("/db-test")
async def db_test():   
    # Example query to test DB connection
    try:
        cur.execute("SELECT * FROM some_table LIMIT 1")  # Replace with a valid query
        result = cur.fetchone()
        return {"db_result": result}
    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]  # Get column headers
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))  # Convert rows into a list of dictionaries
        return json_data
    except mysql.connector.Error as e:
        return {"Error": "MySQL Error: " + str(e)}

@app.get('/songs')
def get_songs():
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
        cur.execute(query)  # Execute the query
        headers = [x[0] for x in cur.description]  # Get column headers
        results = cur.fetchall()  # Fetch all rows
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))  # Convert rows into a list of dictionaries
        return json_data
    except mysql.connector.Error as e:
        return {"Error": "MySQL Error: " + str(e)}

