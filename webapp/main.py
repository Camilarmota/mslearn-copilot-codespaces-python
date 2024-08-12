import os   
import base64   
import hashlib
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

# Modelo Pydantic
class GenerateRequest(BaseModel):
    inputText: str


class Body(BaseModel):
    length: Union[int, None] = 20


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