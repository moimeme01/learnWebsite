import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, Cookie, Body
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Table, Column, String, MetaData
from databases import Database
from pyngrok import ngrok
import threading
import uvicorn


# Absolute path to front-end folder, relative to main.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Goes up from Backend/ to LearnWebsite/
FRONTEND_DIR = os.path.join(BASE_DIR, "front-end")

DATABASE_URL = "sqlite:///./users.db"

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("ip", String, primary_key=True),
    Column("username", String, nullable=False),
)

database = Database(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # starting up
    await database.connect()
    query = """
    CREATE TABLE IF NOT EXISTS users (
    ip TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    gameCode INTEGER);
    """
    await database.execute(query)

    yield

    # shutting down
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.mount("/front-end", StaticFiles(directory=FRONTEND_DIR), name="front-end")
ip_username_map = {}









@app.get("/", response_class=HTMLResponse)
async def root(request: Request, response: Response, user_id: str | None = Cookie(default=None)):
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)

@app.post("/register-user")
async def register_user(request: Request, data: dict = Body(...)):
    username = data.get("username")
    client_ip = request.client.host

    # For SQLite UPSERT alternative:
    query = f"""
    INSERT INTO users (ip, username, gameCode)
    VALUES (:ip, :username, None)
    ON CONFLICT(ip) DO UPDATE SET username=excluded.username;
    """
    await database.execute(query=query, values={"ip": client_ip, "username": username, "gameCode": 0})

    return JSONResponse({"message": f"User: {username}, registered with IP: {client_ip}"})


@app.get("/waitingroom", response_class=HTMLResponse)
async def read_root(request: Request):
    index_path = os.path.join(FRONTEND_DIR, "waitingroom.html")
    return FileResponse(index_path)








# Fonction pour lancer ngrok
def start_ngrok():
    public_url = ngrok.connect(8000, bind_tls=True)
    print(f"🌍 Public URL: {public_url}")

if __name__ == "__main__":
    # Lancer ngrok dans un thread séparé
    threading.Thread(target=start_ngrok).start()
    # Lancer FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)