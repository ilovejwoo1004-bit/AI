from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

## 1) 카프카 프로듀서 객체 생성
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda data: json.dumps(data).encode('utf-8')
)

print("=" * 60)
print("kafka sensor producer")
print("topic : sensor-data")
print("=" * 60)

## 2) 센서 데이터 전송
while True:
    sensor_data = {
        # 센서를 구분하기 위한 id
        "sensor_id": "motor_01",
        # 모터 온도
        "temperature": round(random.uniform(60,90),2),
        # 진동값 1~7 mm/s
        "vibration": round(random.uniform(1,7),2),
        # 모터 rpm
        "rpm": random.randint(1600,1900),
        # 데이터가 발생한 현재 시간
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # topic으로 데이터를 전송
    producer.send("sensor-data", value=sensor_data)  # json -> bytes 변환

    # kafka 버퍼의 데이터 즉시 전송
    producer.flush()

    # 출력
    print("kafka 전송 완료")
    print(
        f"sensor={sensor_data['sensor_id']} | "
        f"temperature={sensor_data['temperature']} ℃ | "
        f"vibration={sensor_data['vibration']} mm/s | "
        f"rpm={sensor_data['rpm']} | "
        f"timestamp={sensor_data['timestamp']}"
    )

    print("-" * 60)

    # 2초마다 새로운 데이터 전송
    time.sleep(2)
