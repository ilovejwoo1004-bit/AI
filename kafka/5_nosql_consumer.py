#=========================================================
'''
kafka의 센서 데이터 topic에서 메세지를 가져온 후
mongodb에 저장하는 consumer 프로그램
'''
#=========================================================

from kafka import KafkaConsumer
from pymongo import MongoClient

import json


## 1) MongoDB 서버 연결
mongo_client = MongoClient("mongodb://localhost:27017/")  # 기본 접속 url

db = mongo_client["factory_db"]   # factory_db 데이터베이스 생성 및 선택

collection = db["sensor_data"]    # collection 생성


## 2) kafka 객체 생성
consumer = KafkaConsumer(
    "sensor-data",                     # topic 네임 정의
    bootstrap_servers=["localhost:9092"],    # kafka broker 주소
    auto_offset_reset="latest",              # 순차 데이터 처리
    enable_auto_commit=True,                 # kafka consumer가 어디까지 메세지를 읽었는지 자동으로 기록
    group_id="mongodb-consumer-group",       # consumer group 이름
    # kafka bytes > utf8 문자열 > json > python dict
    value_deserializer=lambda data:json.loads(data.decode("utf-8"))
)

print("=" * 60)
print("Kafka → MongoDB Consumer 시작")
print("Topic      : sensor-data")
print("Database   : factory_db")
print("Collection : sensor_data")
print("=" * 60)

## 3) 데이터 수신
for message in consumer:
    data = message.value    # python dictionary
    print("메세지 수신")
    print(
        f"topic={message.topic} | "
        f"partition={message.partition} | "
        f"offset={message.offset}"
    )

    print(
        f"Sensor={data['sensor_id']} | "
        f"temp={data['temperature']} ℃ | "
        f"vibration={data['vibration']} mm/s | "
        f"rpm={data['rpm']}"
    )

    ## 4) 간단한 양/불 판정 로직
    # 온도가 80도 이상이면 Warning
    if data['temperature'] >= 80:
        data['status'] = 'Warning'
    else:
        data['status'] = 'Normal'

    ## 5) MongoDB에 데이터 저장
    result = collection.insert_one(data)

    ## 6) 저장 결과 출력
    print(
        f"[mongodb 저장 완료] "
        f"_id={result.inserted_id} | "
        f"Status={data['status']}"
    )

    print("-" * 60)
