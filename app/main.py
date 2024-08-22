#libraries
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_302_FOUND
import os
from model import cal, bubble
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import sqlite3
import uuid
import aiofiles

app = FastAPI()

# Defining the directories
templates_directory = os.path.join(os.getcwd(), "templates")
static_directory = os.path.join(os.getcwd(), "static")
model_directory = os.path.join(os.getcwd(), "model")
database_directory = os.path.join(os.getcwd(), "db")

# Template and static files
app.mount("/static", StaticFiles(directory=static_directory), name="static")
templates = Jinja2Templates(directory=templates_directory)

# Load the deep learning model
model_path = os.path.join(model_directory, 'fruit_model.h5')
model = load_model(model_path)

labels = {
    0: 'apple',
    1: 'banana',
    2: 'beetroot',        
    3: 'bell pepper',     
    4: 'cabbage',         
    5: 'capsicum',        
    6: 'carrot',          
    7: 'cauliflower',     
    8: 'chilli pepper',   
    9: 'corn',            
    10: 'cucumber',       
    11: 'eggplant',       
    12: 'garlic',         
    13: 'ginger',         
    14: 'grapes',         
    15: 'jalapeno',       
    16: 'kiwi',
    17: 'lemon',
    18: 'lettuce',        
    19: 'mango',
    20: 'onion',          
    21: 'orange',
    22: 'paprika',        
    23: 'pear',           
    24: 'peas',           
    25: 'pineapple',      
    26: 'pomegranate',    
    27: 'potato',         
    28: 'raddish',        
    29: 'soy beans',      
    30: 'spinach',        
    31: 'sweetcorn',      
    32: 'sweetpotato',    
    33: 'tomato',         
    34: 'turnip',         
    35: 'watermelon'
}

# Database connection
database_url = os.path.join(database_directory, "fastapi.db")

def get_db(request: Request):
    return request.state.db

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    try:
        request.state.db = sqlite3.connect(database_url, check_same_thread=False)
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_user(db, identifier: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE name=? OR email=?", (identifier, identifier))
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
async def login(request: Request, name: str = Form(None), email: str = Form(None), password: str = Form(...), db = Depends(get_db)):
    identifier = name if name else email
    user = get_user(db, identifier)
    if user:
        if user["password"] == password:
            return RedirectResponse(url="/home", status_code=HTTP_302_FOUND)
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)


# Routes
@app.get("/home", response_class=HTMLResponse)
async def read_root(request: Request, result: str = None, bubble_result: str = None, image_result: str = None, uploaded_image_url: str = None):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": result, 
        "bubble_result": bubble_result,
        "image_result": image_result,
        "uploaded_image_url": uploaded_image_url
    })

@app.post("/calculate")
async def calculate(request: Request, number1: str = Form(...), number2: str = Form(...)):
    try:
        result = cal.add(float(number1), float(number2))
    except ValueError:
        result = "Invalid input"
    return RedirectResponse(url=f"/home?result={result}", status_code=HTTP_302_FOUND)

@app.post("/bubblesort")
async def bubblesort(request: Request, numbers: str = Form(...)):
    try:
        number_list = [int(x) for x in numbers.split()]
        sorted_list = bubble.bubble_sort(number_list)
        bubble_result = ' '.join(map(str, sorted_list))
    except ValueError:
        bubble_result = "Invalid input"
    return RedirectResponse(url=f"/home?bubble_result={bubble_result}", status_code=HTTP_302_FOUND)

@app.post("/predict_image")
async def predict_image(request: Request, file: UploadFile = File(...)):
    try:
        # Generate a safe filename and save the file
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f"{uuid.uuid4()}{file_extension}"
        file_location = os.path.join(static_directory, safe_filename)
        
        async with aiofiles.open(file_location, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Preprocess the image and predict
        img = image.load_img(file_location, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])

        result = labels.get(predicted_class, "Unknown")
        image_url = f"/static/{safe_filename}"

        return RedirectResponse(url=f"/home?image_result={result}&uploaded_image_url={image_url}", status_code=HTTP_302_FOUND)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logout")
async def logout(request: Request):
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    db.commit()
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
