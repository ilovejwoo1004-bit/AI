#=========================================================================
# Producer가 kafka topic으로 0.1초다마 데이터를 보내고,
# consumer가 같은 topic의 데이터를 초당 약 10건 수신하는 tps 출력
#=========================================================================
from random import random

## 1) import
from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

## 2) kafka producer 객체 생성
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda data: json.dumps(data).encode("utf-8")
)

## 3) 데이터를 전송할 topic 지정
topic_name = "press-force"
seq = 0    # 메시지에 순번을 지정하기 위한 변수

# producer 시작 메세지 출력
print("producer 시작: 0.1초마다 1건, 초당 약 10건을 전송합니다.")

## 4) 데이터 강제 종료까지 무한 전송
while True:
    seq = seq + 1  # 메세지 순번을 1씩 증가시킴
    force = random.uniform(130,150)

    # 5% 확률로 이상 force 데이터를 발생시킬
    if random.random() < 0.05:
        force = random.uniform(175,210)   # 175~210 사이로 이상치를 크게 증가시킴


    # 메세지 구성
    message = {
        "seq": seq,   # 메시지 순번
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],  # 현재 시간을 밀리초 단위까지 문자열로 저장
        "machine_id": "press_01",           # 설비 id
        "force": round(force, 2)                 # force 값을 소수점 둘 째 자리까지 반올림
    }

    # kfka topic으로 메세지를 전송
    producer.send(topic_name, value=message)
    producer.flush()

    print(f"전송 seq={message['seq']}, force={message['force']}")

    # 0.1초마다 데이터 전송 (1초에 약 10건 데이터 전송)
    time.sleep(0.1)







