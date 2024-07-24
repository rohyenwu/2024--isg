from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database import get_db_connection, get_summary_reviews

# FastAPI 애플리케이션 생성
app = FastAPI()

# @app.get("/review", response_class=JSONResponse)
# async def get_review(request: Request, gamename: str):
#         get_db_connection()
#         reviews=get_summary_reviews(gamename)
#         reviews=1
#         if not reviews:
#             return JSONResponse(content={"error": f"게임 '{gamename}'에 대한 리뷰 정보를 찾을 수 없습니다."}, status_code=404)
#         else:
#             return reviews
 


