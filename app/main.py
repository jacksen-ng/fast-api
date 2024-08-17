from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_302_FOUND
from model import cal
import os
import sqlite3

app = FastAPI()

templates_directory = os.path.join(os.getcwd(), "templates")
static_directory = os.path.join(os.getcwd(), "static")
model_directory = os.path.join(os.getcwd(), "model")
database_directory = os.path.join(os.getcwd(), "db")

database_url = os.path.join(database_directory, "fastapi.db")

def get_db(request: Request):
    return request.state.db

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = sqlite3.connect(database_url, check_same_thread=False)
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_user(db, name: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE name=? OR email=?", (name, name))
    row = cursor.fetchone()
    if row:
        return {"name": row[1], "email": row[2], "password": row[3]}
    return None

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(name: str = Form(...), password: str = Form(...), db = Depends(get_db)):
    user = get_user(db, name)
    if not user or user["password"] != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return RedirectResponse(url="/home", status_code=HTTP_302_FOUND)

app.mount("/static", StaticFiles(directory=static_directory), name="static")
templates = Jinja2Templates(directory=templates_directory)

@app.get("/home", response_class=HTMLResponse)
async def read_root(request: Request, result: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.post('/calculate')
async def calculate(request: Request, number1: str = Form(...), number2: str = Form(...)):
    result = cal.add(number1, number2)
    return RedirectResponse(url=f"/home?result={result}", status_code=HTTP_302_FOUND)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
