from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# 현재 스크립트 파일의 절대 경로
current_dir = Path(__file__).resolve().parent

# 프로젝트의 루트 디렉토리
root_dir = current_dir.parent.parent  # current_dir의 부모 디렉토리의 부모 디렉토리를 root_dir로 정의

# templates 디렉토리의 절대 경로
templates_dir = root_dir / "sig-project" / "templates"

# Jinja2Templates 초기화
templates = Jinja2Templates(directory=str(templates_dir))

# index.html을 렌더링하는 엔드포인트
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
