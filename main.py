from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db',check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                createAt TEXT NOT NULL
            );
            """)

app = FastAPI()

@app.post("/items")
async def create_item(image:UploadFile,
                 title:Annotated[str,Form()],
                 price:Annotated[int,Form()],
                 description:Annotated[str,Form()],
                 place:Annotated[str,Form()],
                 createAt:Annotated[str,Form()]):
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items (image, title, price, description, place, createAt)
                VALUES ('{image_bytes.hex()}','{title}',{price},'{description}','{place}','{createAt}')
                """)
    con.commit()
    return "200"

@app.get('/items')
async def get_items():
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                SELECT * FROM items;
                """).fetchall()
    
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    res = cur.execute(f"""
                      SELECT image FROM items WHERE id={item_id}
                      """).fetchone()[0]
    return Response(content=bytes.fromhex(res), media_type='image/*')


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")