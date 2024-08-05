from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os  # 환경 변수를 읽기 위해 추가
from database import get_summary_reviews
from typing import Dict

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

# OpenAI API 키 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # 환경 변수에서 API 키를 가져옴
if not OPENAI_API_KEY:
    raise ValueError("API key not found in environment variables")

openai.api_key = OPENAI_API_KEY

# 모델 선택 및 번역
model = "gpt-3.5-turbo"

async def translate_text(text: str, target_language: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a translation assistant. Translate the following text into the specified target language."},
                {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
            ],
            max_tokens=500
        )
        translated_text = response.choices[0].message['content'].strip()
        if not translated_text:
            raise ValueError("No content in response")
        
    except openai.OpenAIError as e:
        # 상세한 오류 메시지 출력
        print(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except ValueError as e:
        # 상세한 값 오류 메시지 출력
        print(f"Value error: {e}")
        raise HTTPException(status_code=500, detail=f"Value error: {e}")
    
    return translated_text

@app.get("/review", response_class=JSONResponse)
async def get_review(gamename: str = Query(..., alias="gamename"), target_language: str = Query("ko")):
    print(f"Received game name: {gamename}")  # 콘솔에 게임 이름 출력 
    reviews = get_summary_reviews(gamename)
    
    if not reviews:
        return JSONResponse(content={"error": f"게임 '{gamename}'에 대한 리뷰 정보를 찾을 수 없습니다."}, status_code=404)
    
    reviews_json = reviews.dict()  # Pydantic 모델을 dict로 변환
    print(f"Reviews: {reviews_json}")
    
    # 리뷰 번역
    translated_reviews = {}
    categories = ["graphic", "sound", "story", "creativity", "graphicNative", "soundNative", "storyNative", "creativityNative"]
    
    for category in categories:
        original_review = reviews_json.get(category, "")
        if original_review:  # 비어 있는 리뷰는 번역하지 않음
            translated_review = await translate_text(original_review, target_language)
        else:
            translated_review = ""
        translated_reviews[category] = translated_review

    # 번역된 리뷰를 콘솔에 출력
    print(f"Translated Reviews: {translated_reviews}")

    return translated_reviews
