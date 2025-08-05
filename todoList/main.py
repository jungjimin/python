from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

# FastAPI 앱 생성
app = FastAPI()

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 할 일 항목 모델
class TodoItem(BaseModel):
    category: str
    task: str

# 데이터 저장소 (메모리)
todos_db = {
    "반영": [],
    "가맹점문의": [],
    "기타": []
}

# 홈 페이지 렌더링
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos_db": todos_db})

# 할 일 추가 API
@app.post("/add_todo", response_model=TodoItem)
async def add_todo(todo: TodoItem):
    if todo.category not in todos_db:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    todos_db[todo.category].insert(0, todo.task)  # 최신 항목을 맨 앞에 추가
    return todo