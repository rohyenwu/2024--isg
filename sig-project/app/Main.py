from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database import get_db_connection, get_summary_reviews

# FastAPI 애플리케이션 생성
app = FastAPI()

# 현재 스크립트의 경로
current_dir = Path(__file__).resolve().parent

# 프로젝트의 루트 디렉토리
root_dir = current_dir.parent.parent  # 현재 디렉토리의 부모 디렉토리의 부모 디렉토리를 root_dir로 정의

# templates 디렉토리의 절대 경로
templates_dir = root_dir / "sig-project" / "templates"

# 정적 파일을 제공하기 위해 StaticFiles를 사용하여 /static 엔드포인트에 templates_dir 디렉토리 마운트
app.mount("/static", StaticFiles(directory=str(templates_dir)), name="static")


# Jinja2Templates 초기화
templates = Jinja2Templates(directory=str(templates_dir))
@app.get("/")
async def root_read():
    return templates.TemplateResponse("index.html") 


@app.get("/game")
async def move_contact(request: Request):
    return templates.TemplateResponse

@app.get("/review", response_class=JSONResponse)
async def get_review(request: Request, gamename: str):
        get_db_connection()
        reviews=get_summary_reviews(gamename)
        reviews=1
        if not reviews:
            return JSONResponse(content={"error": f"게임 '{gamename}'에 대한 리뷰 정보를 찾을 수 없습니다."}, status_code=404)
        else:
            return reviews
 


