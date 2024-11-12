from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Dict, Union
import cowsay
import random
import requests
import sqlite3

# Initialize FastAPI application with /v1 prefix for API versioning
app = FastAPI(
    title="Random Jokes API",
    description="A simple API for storing and retrieving jokes.",
    version="1.0.0"
)

# Database setup
DATABASE = "jokes.db"

def get_db_connection() -> sqlite3.Connection:
    """
    Establish and return a database connection.

    Returns:
        sqlite3.Connection: A connection object for the SQLite database.
    """
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Create jokes table if it doesn't exist
with get_db_connection() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS jokes (
        id INTEGER PRIMARY KEY,
        created DATETIME DEFAULT current_timestamp,
        setup TEXT NOT NULL,
        punchline TEXT NOT NULL
    )
    """)
    conn.commit()

# Joke schema for request/response validation
class Joke(BaseModel):
    setup: str
    punchline: str

# Endpoints
@app.get("/api/v1/", response_class=Response, responses={200: {"content": {"text/plain": {}}}})
async def root() -> Response:
    """
    Return a funny greeting message using cowsay.

    Returns:
        Response: A plain text response with a cowsay message.
    """
    retval = cowsay.get_output_string(random.choice(cowsay.char_names), "Joke's on you!")
    return Response(content=retval, media_type="text/plain")

@app.get("/api/v1/random", response_model=Dict[str, str])
async def get_random_joke() -> Union[Dict[str, str], HTTPException]:
    """
    Fetch a random joke from an external API and save it to the local database.

    Returns:
        dict: A dictionary containing the joke setup and punchline.
    Raises:
        HTTPException: If the external API fails to retrieve a joke.
    """
    response = requests.get('https://simple-joke-api.deno.dev/random')
    if response.status_code == 200:
        json_data = response.json()
        with get_db_connection() as conn:
            conn.execute("INSERT INTO jokes (setup, punchline) VALUES (?, ?)", (json_data["setup"], json_data["punchline"]))
            conn.commit()
        return json_data
    else:
        raise HTTPException(status_code=404, detail="Failed to retrieve data from the external API")

@app.get("/api/v1/all", response_model=List[Dict[str, Union[int, str]]])
async def get_all_jokes() -> List[Dict[str, Union[int, str]]]:
    """
    Retrieve all jokes from the local database.

    Returns:
        list: A list of dictionaries, each containing joke details.
    """
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM jokes")
        jokes = [dict(row) for row in cursor.fetchall()]
    return jokes

@app.post("/api/v1/new", response_model=Dict[str, str])
async def insert_joke(joke: Joke) -> Dict[str, str]:
    """
    Add a new joke to the database.

    Args:
        joke (Joke): The joke data to add to the database.

    Returns:
        dict: A success message.
    """
    with get_db_connection() as conn:
        conn.execute("INSERT INTO jokes (setup, punchline) VALUES (?, ?)", (joke.setup, joke.punchline))
        conn.commit()
    return {"status": "Joke added successfully"}

@app.delete("/api/v1/delete/{joke_id}", response_model=Dict[str, str])
async def delete_joke(joke_id: int) -> Dict[str, str]:
    """
    Delete a joke by its ID.

    Args:
        joke_id (int): The ID of the joke to delete.

    Returns:
        dict: A success message if the joke is deleted.
    Raises:
        HTTPException: If the joke with the given ID is not found.
    """
    with get_db_connection() as conn:
        result = conn.execute("DELETE FROM jokes WHERE id = ?", (joke_id,))
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Joke with id {joke_id} not found")
        conn.commit()
    return {"status": "Joke deleted successfully"}

@app.put("/api/v1/update/{joke_id}", response_model=Dict[str, str])
async def update_joke(joke_id: int, joke: Joke) -> Dict[str, str]:
    """
    Update an existing joke by its ID.

    Args:
        joke_id (int): The ID of the joke to update.
        joke (Joke): The updated joke data.

    Returns:
        dict: A success message if the joke is updated.
    Raises:
        HTTPException: If the joke with the given ID is not found.
    """
    with get_db_connection() as conn:
        result = conn.execute("UPDATE jokes SET setup = ?, punchline = ? WHERE id = ?", (joke.setup, joke.punchline, joke_id))
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Joke with id {joke_id} not found")
        conn.commit()
    return {"status": "Joke updated successfully"}

#if __name__ == "__main__":
#    import uvicorn
#    # Just to make sure that the app is alive
#    print(cowsay.get_output_string('cow', 'Hello World!'))
#    workers = 2 # how many workers to use for serving the user requests
#    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True, workers=workers)
