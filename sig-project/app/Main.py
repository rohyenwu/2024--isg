from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI,Query
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database import get_db_connection, get_summary_reviews
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 생성
app = FastAPI()
# CORS 설정
origins = [
    "http://localhost:3000",  # React 개발 서버
    # 필요한 다른 도메인 추가 가능
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 오리진 목록
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드 (GET, POST 등)
    allow_headers=["*"],  # 허용할 HTTP 헤더
)


    
@app.get("/review", response_class=JSONResponse)
async def get_review(gamename: str = Query(..., alias="gamename")):
    print(f"Received game name: {gamename}")  # 콘솔에 게임 이름 출력 
    reviews=get_summary_reviews(gamename)
    if not reviews:
        return JSONResponse(content={"error": f"게임 '{gamename}'에 대한 리뷰 정보를 찾을 수 없습니다."}, status_code=404)
    else:
        return reviews
 



