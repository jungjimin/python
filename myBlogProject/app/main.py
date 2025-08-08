from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, database, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts})

@app.get("/posts/new")
def create_post_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/posts/new")
def create_post(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    post = models.Post(title=title, content=content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return RedirectResponse(url="/", status_code=303)

@app.get("/posts/{post_id}")
def read_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("detail_post.html", {"request": request, "post": post})