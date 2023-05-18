from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, session_local
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def createBlog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def deleteBlog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with {id} not available')
    blog.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def updateBlog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with {id} not available')
    blog.update(request)
    db.commit()
    return "successfully updated"

@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def showBlog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with {id} not available')
    return blog

@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=['users'])
def getUser(id, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with {id} not available')
    return user