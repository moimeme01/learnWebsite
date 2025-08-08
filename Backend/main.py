import os
import uuid
from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pyngrok import ngrok
import threading
import uvicorn


# Absolute path to front-end folder, relative to main.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Goes up from Backend/ to LearnWebsite/
FRONTEND_DIR = os.path.join(BASE_DIR, "front-end")



app = FastAPI()
app.mount("/front-end", StaticFiles(directory=FRONTEND_DIR), name="front-end")
USER_ID_COOKIE = "user_id"


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, response: Response, user_id: str | None = Cookie(default=None)):
    # Assign user_id cookie if not present
    if not user_id:
        user_id = str(uuid.uuid4())
        response.set_cookie(key=USER_ID_COOKIE, value=user_id, httponly=True)
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)

@app.get("/user", response_class=JSONResponse)
async def get_user(user_id: str | None = Cookie(default=None)):
    if not user_id:
        return JSONResponse({"error": "User ID cookie not found"}, status_code=404)
    return {"user_id": user_id}


@app.get("/card1", response_class=HTMLResponse)
async def read_root(request: Request):
    index_path = os.path.join(FRONTEND_DIR, "indexCard1.html")
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