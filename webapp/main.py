import os   
import base64   
import hashlib
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

# Modelo Pydantic
class GenerateRequest(BaseModel):
    inputText: str


class Body(BaseModel):
    length: Union[int, None] = 20


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Union[int, None] = None


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
# Create a FastAPI endpoint that accepts a POST request with a JSON body containing a single field called "text" and returns a checksum of the text
async def generate_checksum(request: GenerateRequest):
    checksum = hashlib.md5(request.inputText.encode()).hexdigest()
    return JSONResponse(content={"checksum": checksum})


@app.get('/submit')
def submit():
    html_path = join(static_path, "submit.html")
    return FileResponse(html_path)


@app.get('/form')
def form():
    html_path = join(static_path, "form.html")
    return FileResponse(html_path)


# Modelo Pydantic para a requisição
class TextRequest(BaseModel):
    text: str


# Create a FastAPI endpoint that accepts a POST request with a JSON body containing a single field called "text" and returns a checksum of the text
@app.post("/checksum")
async def generate_checksum(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    checksum = hashlib.md5(request.text.encode()).hexdigest()
    return {"checksum": checksum}