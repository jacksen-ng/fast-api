from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
from model import cal
import os

app = FastAPI()

templates_directory = os.path.join(os.getcwd(), "templates")
static_directory = os.path.join(os.getcwd(), "static")
model_directory = os.path.join(os.getcwd(), "model")

app.mount("/static", StaticFiles(directory=static_directory), name="static")
templates = Jinja2Templates(directory=templates_directory)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, result: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.post('/calculate')
async def calculate(request: Request, number1: str = Form(...), number2: str = Form(...)):
    result = cal.add(number1, number2)
    return RedirectResponse(url=f"/?result={result}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
