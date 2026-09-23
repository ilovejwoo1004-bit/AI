#======================================================
# Fast API 기본 실습
# - GET 요청 -> 서버 상태 확인
# - POST 요청 -> 사용자 데이터를 받아 처리 후 응답
#======================================================

## 1. import
from fastapi import FastAPI
from pydantic import BaseModel     # 입력 데이터 유효성 검사용
from typing import Optional
import uvicorn

## 2. Fast API 앱 인스턴스 생성
# app 객체는 서버의 중심이며, 모든 api 엔드포인트를 여기에 등록
app = FastAPI(
    title="Fast API 기본 실습",
    description="기본 실습",
    version="1.0.0"
)

## 3. 데이터 모델 정의 (post 요청 시)
class Item(BaseModel):
    name : str                               # 필수 : 아이템 이름
    price: float                        # 필수 : 가격
    description: Optional[str] = None        # 선택 : 아이템 설명 내용

## 4. 기본 엔트포인트 (GET 요청)
# URL : http://192.168.0.174:8000/
@app.get("/")
def read_root():
    '''
    서버 상태를 확인하는 기본 엔드포인트
    브라우저 or curl로 get 요청 시 메세지 반환
    '''
    return {"message": "Fast API 서버가 정상적으로 동작 중입니다."}

## 5. 단순 get 요청 (query parameter 사용)
# URL : http://192.168.0.174:8000/hello?name=길동
@app.get("/hello")
def say_hello(name: str = "사용자"):
    '''
    get 요청시 url 파라미터로 이름을 받아 인사 메세지를 반환
    예) /hello?name=길동
    '''
    return {"message": f"안녕하세요 {name}님!"}

## 6. post 요청 (body 데이터 받기)
# URL : http://192.168.0.174:8000/items
@app.post("/items")
def create_item(item: Item):
    '''
    post 요청 예시 (json body)
    {
    "name": "노트북",
    "price": 1,500,000
    "description": "ai 모델 학습용 고성능 노트북"
    }
    '''

    # 간단한 세금계산 로직
    total_price = item.price * 1.1

    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "total_with_tax": total_price,
        "message": f"{item.name} 상품이 성공적으로 등록되었습니다."
    }

## 7. Fast API 서버 실행(uvicorn)
if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.174", port=8000)
