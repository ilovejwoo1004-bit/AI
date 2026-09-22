#=========================================================================
# Producer가 kafka topic으로 1초다마 데이터를 보내고,
# consumer가 같은 topic의 데이터를 받는 것 확인
#=========================================================================

## 1) import
from kafka import KafkaConsumer
import json

## 2) kafka 객체 생성
consumer = KafkaConsumer(
    "press-force",                                                              # 구독할 topic 이름 정의
    bootstrap_servers=["localhost:9092"],                                       # broker 주조 지정
    auto_offset_reset="latest",                                                 # consumer가 처음 실행 될 때 최신 데이터로부터 읽도록 설정
    group_id="basic-consumer-group",                                            # consumer 그룹 id 지정 > 같은 그룹 id를 가진 consumer가 데이터를 나눠서 읽음
    value_deserializer=lambda data: json.loads(data.decode("utf-8"))   # kafka에서 받은 bytes 데이터를 utf-8 문자열로 바꾸고 json을 dict로 변환
)

# consumer가 정상적으로 시작되었음을 출력
print("consumer_basic 시작: press-force Topic 데이터를 수신합니다.")

## kafka topic에서 메세지가 들어올 때마다 반복 실생
for message in consumer:
    data = message.value
    print("수신: ", data)

