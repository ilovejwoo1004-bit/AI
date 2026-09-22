import socket
import struct               # 데이터 길이를 byte 형태로 변환하기 위한 라이브러리
import json
import numpy as np          # 배열 연산
import tensorflow as tf
from PIL import Image       # 이미지 처리
from io import BytesIO      # 메모리상의 이미지 처리

# =============================================
# cifar 10 클래스 정의
# =============================================
CLASS_NAMES = [
    "airplane",
    "autombile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]

# =============================================
# 학습된 모델 로드
# =============================================
print("AI 모델 로딩 시작")

# 학습 결과 파일 읽어오기
model = tf.keras.models.load_model('./model/cifar10_model.h5')
print("AI 모델 로딩 완료")

# =============================================
# 지정 크기만큼 데이터 수신하는 함수
# =============================================
def recv_all(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))

        if not packet:
            return None

        data += packet

    return data

# =============================================
# 이미지 추론 모듈 함수
# =============================================
def predict_image(image_bytes):
    '''
    입력 > 이미지 byte > 출력 > 분류 결과
    '''
    ## byte --> PIL Image
    image = Image.open(BytesIO(image_bytes))

    ## RGB 변환
    image = image.convert('RGB')

    ## cifar 10 이미지 크기 맞춤
    image = image.resize((32, 32))

    ## numpy 배열 변환
    image = np.array(image)

    ## 정규화
    image = image / 255.0 # 0~1 사이의 값으로 정규화

    ## 배치 차원 추가
    image = np.expand_dims(image, axis=0)

    ## shape 확인
    print("입력 shape: ", image.shape)

    ## 모델 추론
    pred = model.predict(
        image,
        verbose=0
    )

    #예측결과 수행
    print("예측 확률: ", pred)

    ## 가장 높은 확률 찾기
    class_idx = np.argmax(pred)
    confidence = np.max(pred)
    print("예측 클래스 : ", class_idx)
    print("신뢰도 : ", confidence)

    ## 결과 생성
    result = {
        "class_id": int(class_idx),
        "class_name": CLASS_NAMES[int(class_idx)],
        "confidence": float(confidence)
    }

    return result

# =============================================
# 서버 설정
# =============================================
HOST = '192.168.0.174'  # 서버의 ip 주소
PORT = 9998

# =============================================
# tcp 소켓 객체 생성
# =============================================
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("소켓 생성 완료")

# =============================================
# 포트 바인딩
# =============================================
server_socket.bind((HOST, PORT))
print("포트 바인딩 완료")

# =============================================
# 클라이언트 접속 대기
# =============================================
server_socket.listen(5)
print(f"AI 서버 시작: {HOST}:{PORT}")

# =============================================
# 데이터 송수신 무한 루프
# =============================================
while True:
    print("\n클라이언트 접속 대기 중")
    # 클라이언트 접속 확인 (accept())
    client_socket, addr = server_socket.accept()
    print("클라이언트 접속: ", addr)

    try:
        # 이미지 크기 수신  <-- 클라이언트에서 먼저 이미지 크기를 보냄 예) 125000 byte
        header = recv_all(client_socket, 4)   # 4byte 씩 데이터 받음

        if header is None:
            print("서버 연결 종료 또는 데이터 수신 실패")
            break

        # 4byte -> 정수 변환
        image_size = struct.unpack('>I', header)[0]
        print("이미지 크기: ", image_size)

        # 이미지 수신
        image_bytes = recv_all(client_socket, image_size)
        print("이미지 수신 완료")

        # AI 추론
        result = predict_image(image_bytes)
        print("추론 결과 : ", result)

        # json 변환
        result_json = json.dumps(result, ensure_ascii=False).encode()

        # 결과 길이 전송
        client_socket.sendall(struct.pack('>I', len(result_json)))
        print("결과 길이 전송 완료")

        # 결과 데이터 전송
        client_socket.sendall(result_json)
        print("결과 데이터 전송 완료")

    except Exception as e:
        print("오류 발생 : ", e)

    finally:
        # 소켓 연결종료
        client_socket.close()
        print("클라이언트 연결 종료")










