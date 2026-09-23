# ============================================================
# FastAPI 기반 스팸 메시지 판별 서버
#
# 기능
# 1. 클라이언트로부터 text를 JSON 형태로 전달받음
# 2. 스팸 여부를 분석
# 3. spam, confidence 결과를 JSON으로 반환
# ============================================================
from urllib import request

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# ------------------------------------------------------------
# 1. FastAPI 객체 생성
# ------------------------------------------------------------
app = FastAPI(
    title="Spam Classification",
    description="문장을 입력받아 스팸 여부를 판별하는 api",
    version="1.0"
)

# ------------------------------------------------------------
# 2. 클라이언트 요청 데이터 구조 정의
# ------------------------------------------------------------
class SpamRequest(BaseModel):
    text: str

# ------------------------------------------------------------
# 3. 스팸 판별 함수
# ------------------------------------------------------------
def predict_spam(text):
    # 스팸 메세지에서 자주 등장하는 단어에 대한 필터 정의
    spam_keywords = [
        "무료",
        "당첨",
        "쿠폰",
        "이벤트",
        "대출",
        "광고",
        "클릭",
        "수익",
        "투자"
    ]

    # 발견된 스팸 키워드 개수
    count = 0

    for keyword in spam_keywords:
        if keyword in text:
            count += 1

    # confidence 계산 / 키워드 하나당 0.2씩 적용 / 최대값은 1.0
    confidence = round(min(count * 0.2, 1.0),2)    # min(count 6 * 0.2 = 1.2, 1.0) --> 1.0

    # confidence가 0.4이상이면 스팸으로 판정
    spam = confidence > 0.4

    return spam, confidence

# ------------------------------------------------------------
# 4. 스팸 분석 API
# ------------------------------------------------------------
@app.post("/spam")
def spam_detection(request: SpamRequest):

    # 입력값 유효성 검증
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="분석할 문장을 입력해주세요"
        )

    # 스팸 분석
    spam, confidence = predict_spam(request.text)

    # 결과 반환
    return {"text": request.text, "spam": spam, "confidence": confidence}

# ------------------------------------------------------------
# 5. 서버 실행
# ------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.174", port=8000)