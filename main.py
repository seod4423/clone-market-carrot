from fastapi import FastAPI,UploadFile,Form,Response,Depends
from fastapi.responses import RedirectResponse
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

logs = []

SECRET = 'super-secret-key234'
manager = LoginManager(SECRET, '/login')

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

@app.post("/chatroom")
def get_chatroom_message(message: Annotated[str,Form()]):
    newLog = {}
    newLog[len(logs)] = message
    sendLogs = logs  + [newLog]
    logs.append(newLog)
    return JSONResponse(jsonable_encoder(sendLogs))

@app.get("/chatroom")
def get_chatroom():
    return RedirectResponse("/chatroom.html")

@manager.user_loader()
def query_user (data):
    WHERE_STATEMENT = f'''id="{data}"'''
    if type(data) == dict:
        WHERE_STATEMENT = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENT}
                       """).fetchone()
    return user

@app.post("/login")
async def login(id:Annotated[str,Form()],
                password:Annotated[str,Form()]):
    user  = query_user(id)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
        
    access_token = manager.create_access_token(
        data={ 'sub': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']}
            
        }
    )
    return {'access_token': access_token}

@app.post("/signup")
async def signup(id:Annotated[str,Form()],
                 password:Annotated[str,Form()],
                 name:Annotated[str,Form()],
                 email:Annotated[str,Form()]):
    print(id, password, name, email)
    cur.execute(f"""
                INSERT INTO users (id, password, name, email)
                VALUES ('{id}','{password}','{name}','{email}')
                """)
    con.commit()
    return "200"

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
async def get_items(user=Depends(manager)):
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