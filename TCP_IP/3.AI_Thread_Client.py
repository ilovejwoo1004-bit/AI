#=============================================================
# 멀티 클라이언트 지원 api tcp 서버
# - 사용자가 입력한 요청(분석 모드, 입력문장)을 서버로 전송
# - 서버의 분석 결과를 수신 및 출력
#=============================================================

import socket
import json

#------------------------------------
# 1. 서버 접속 정보
#------------------------------------
HOST = '192.168.0.174'  # 서버의 ip 주소
PORT = 9996             # 사용할 포트 번호 (0~65535 중 하나 사용)

#------------------------------------
# 2. 서버 연결 시도
#------------------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("서버에 연결되었습니다. (종료하려면 'exit' 입력) \n")

#------------------------------------
# 3. 메세지 송수신 무한 루프 구성
#------------------------------------
while True:
    mode = input("분석 모드 (length / sentiment / keyword : ").strip()

    if mode.lower() == "exit":
        client_socket.sendall(mode.encode())
        break

    # 분석할 텍스트 입력
    text = input("분석할 문장 입력 : ").strip()

    # 요청 json 구성
    request = {"mode": mode, "text": text}

    # json encoding으로 변환한 byte를 서버로 전송
    client_socket.sendall(json.dumps(request, ensure_ascii=False).encode())

    # 서버 응답 수신
    data = client_socket.recv(1024).decode()
    try:
        response = json.loads(data)
        print(f"\n 서버 응답 : {json.dumps(response, ensure_ascii=False, indent=2)}\n")
    except json.decoder.JSONDecodeError:
        print(f"서버 응답 오류: {data}\n")

#------------------------------------
# 4. 연결 종료
#------------------------------------
client_socket.close()
print("클라이언트 종료 완료")

