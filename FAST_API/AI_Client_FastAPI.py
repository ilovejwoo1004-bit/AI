#==============================================
# AI 클라이언트
'''
- 사용자 입력을 받아서 ai 서버에 분석 요청을 전송
- ai 서버의 분석 결과를 json으로 응답을 받아 콘솔에 출력
'''
#==============================================

import requests  # http 통신
import json      # json 처리

## 1. 서버 주소 설정
SERVER_URL = "http://192.168.0.174:8000/analyze"
print("AI 서버 클라이언트 시작 (종료하려면 'exit' 입력)\n")

## 2. 사용자 입력
while True:
    # 분석 모드 선택
    mode = input("분석 모드 입력 (length / sentiment / keyword): ").strip()

    if mode.lower() == "exit":
        print("클라이언트 종료")
        break

    # 분석할 문장 입력
    text = input("분석할 문장 입력 : ").strip()

    # 요청 데이터 생성(json)
    payload = {"mode": mode, "text": text}

    # post 요청 전송
    try:
        response = requests.post(SERVER_URL, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"서버 연결 오류: {e}\n")
        continue

    # 서버의 응답 메세지 출력
    if response.status_code == 200:
        result = response.json()
        print(f"\n 서버 응답:\n{json.dumps(result, ensure_ascii=False, indent=2)}\n")
    else:
        print(f" 오류 발생: {response.status_code}, {response.text}\n")



