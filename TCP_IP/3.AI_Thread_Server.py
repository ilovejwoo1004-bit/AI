# ============================================================
# 멀티 클라이언트 지원 API TCP 서버
# - 여러 클라이언트가 동시에 접속 가능 (Thread 기반)
# - 각 클라이언트가 json 형태의 분석 요청을 보내면, 서버는 분석 결과(json)을 응답
# ============================================================

import socket
import threading
import json

# ============================================================
# 1. 서버 기본 설정
# ============================================================

HOST = '192.168.0.174'  # 서버의 ip 주소
PORT = 9996             # 사용할 포트 번호 (0~65535 중 하나 사용)
MAX_CLIENTS = 20        # 동시 연결 가능한 최대 클라이언트 수

# ============================================================
# 2. 기본 분석 함수 정의
# ============================================================

def analyze_text(request):
    mode = request.get("mode", "")
    text = request.get("text", "")

    # 1) 문자열 길이 분석
    if mode == "length":
        return {"result": len(text), "desc":f"문자 길이는 {len(text)}입니다."}

    # 2) 감정분석 (간단한 규칙 기반)
    elif mode == "sentiment":
        if any(w in text for w in ["좋아","행복","기쁨","멋져"]):
            sentiment = "positive"
        elif any(w in text for w in ["나빠","싫어","불만","짜증"]):
            sentiment = "negative"
        else:
            sentiment = "neutral"
        return {"result": sentiment, "desc": f"감정 분석 결과: {sentiment}"}

    # 3) 키워드 탐지
    elif mode == "keyword":
        keywords = ["전류상승","속도저하","불량","유량저하","온도상승"]
        found = [k for k in keywords if k in text]
        return {"result": found, "desc": f"발견된 키워드: {','.join(found) if found else '없음'}"}

    # 4) 기타 모드
    else:
        return {"error": f"지원하지 않는 모드입니다: {mode}"}


# ============================================================
# 3. 클라이언트 처리 쓰레드 함수
# ============================================================
def handle_client(client_socket, address):
    '''
    각 클라이언트 연결마다 실행되는 쓰레드 함수
    '''
    print(f"클라이언트 {address} 연결됨")
    while True:
        try:
            # 클라이언트로부터 데이터 수신 (최대 2KB)
            data = client_socket.recv(2048).decode()

            if not data:
                print(f" {address} 연결 끊김")
                break

            if data.lower() == "exit":
                print(f"{address} 종료 요청 수신")
                break

            # json 데이터 파싱
            try:
                request = json.loads(data)
                result = analyze_text(request)
            except json.JSONDecodeError:
                result = {"error": "잘못된 json 형식입니다."}

            # 응답 전송 (json -> bytes)
            response = json.dumps(result, ensure_ascii=False)
            client_socket.sendall(response.encode())
        except ConnectionResetError:
            # 클라이언트가 비정상적으로 종료된 경우
            print(f" {address} 비정상 종료")
            break

    # 연결 종료 처리
    client_socket.close()
    print(f"클라이언트 {address} 세션 종료 완료")

# ============================================================
# 4. 서버 메인 실행부
# ============================================================
def start_server():
    '''
    메인 서버 함수 : 클라이언트 접속 대기하고,
    접속시마다 새로운 쓰레드를 생성하여 handle_client 를 실행
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)

    print(f"AI 서버 실행 중...... {HOST}:{PORT}")
    print(f" 최대 {MAX_CLIENTS}개의 클라이언트 동시 접속 가능\n")

    try:
        while True:
            # 클라이언트 연결 대기
            client_socket, addr = server_socket.accept()

            #쓰레드 생성 및 실행
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, addr), daemon=True
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\n 서버 수동 종료 감지")

    finally:
        server_socket.close()
        print("서버 완전 종료")


# ============================================================
# 5. 실행 시작
# ============================================================
if __name__ == "__main__":
    start_server()