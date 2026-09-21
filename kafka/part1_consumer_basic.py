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
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "press-force",                        # 구독할 topic 이름을 정의
    bootstrap_servers="localhost:9092",         # broker 주소 지정
    auto_offset_reset="latest",                 # consumer가 처음 실행 될 때 최신 데이터로부터 읽도록 설정
    group_id="basic-consumer-group",            # consumer 그룹 id 지정 --> 같은 그룹 id를 가진 consumer는 데이터 나눠서 읽음
    # Kafka에서 받은 bytes 데이터를 UTF-8 문자열로 바꾸고 JSON을 dict로 변환
    value_deserializer=lambda data: json.loads(data.decode("utf-8"))
)

# consumer가 정상적으로 시작되었음을 출력
print("consumer_basic 시작: press-force Topic 데이터를 수신합니다.")

# kafka topic에 메시지가 들어올 때마다 반복 실행
for message in consumer:
    data = message.value
    print("수신:", data)





