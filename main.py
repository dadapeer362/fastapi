from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get('/')
def index():
    return {'data': 'blog list'}

@app.get('/blog/{id}')
def blog(id: int):
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id):
    return {'data': 'hello dadapeer'}

@app.get('/books')
def books(limit = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} books are published'}
    else:
        return {'data': f'{limit} books are not published'}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return f'Blog is created with title {request.title}'

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=9000)