#================================================================
'''
Producer가 Kafka Topic으로 데이터를 보내고,
Consumer가 같은 Topic에서 데이터를 받는 것을 확인

01_producer_basic.py      (실행 1)
        ↓
Kafka Topic: press-force
        ↓
01_consumer_basic.py   (실행 2)
'''
#================================================================
# kafka로 데이터를 보내는 producer 객체를 만들기 위한 클래스
from kafka import KafkaProducer

import json
import random   # 데이터 생성
import time     # 일정 시간마다 데이터를 보내기 위해 사용



# kafka 객체 생성
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],    # kafka 기본 포트 9092
    value_serializer=lambda data: json.dumps(data).encode('utf-8')  # python dict -> json 문자열 -> utf-8 bytes 변환
)

# 데이터를 보낼 kafka Topic 이름 지정
topic = 'press-force'
print("Producer 시작: 1초마다 Force 데이터를 전송합니다.")

# 데이터가 강제 종료될 때까지 계속 반복하여 데이터 전송
while True:
    force = round(random.uniform(130, 150),2)
    message = {
        "machine_id": "press_01",
        "force": force
    }

    # kafka의 press-force Topic으로 message 데이터를 전송
    producer.send(topic, value=message)

    #producer 내부 버퍼에 남아 있는 데이터를 즉시 전송
    producer.flush()

    print("전송:", message)

    # 1초마다 전송
    time.sleep(1)


