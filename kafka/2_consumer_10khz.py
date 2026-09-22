#=========================================================================
# Producer가 kafka topic으로 0.1초다마 데이터를 보내고,
# consumer가 같은 topic의 데이터를 초당 약 10건 수신하는 tps 출력
#=========================================================================

## 1) import
from kafka import KafkaConsumer
import json
import time


## 2) kafka consumer 객체 생성
consumer = KafkaConsumer(
    "press-force",
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    group_id='tps-consumer-group',
    value_deserializer=lambda data: json.loads(data.decode('utf-8'))
)

## 3) 데이터 읽어오기
count_per_second = 0       # 1초동안 수신한 메세지 개수 저장
total_count = 0            # 프로그램 시작 후 전체 수신한 메세지 저장
start_time = time.time()   # TPS 측정 시작 시간을 저장

print("TPS Consumer 시작 : 초당 수신 건수를 계산합니다.")

# 반복적으로 메세지 읽어오기
for message in consumer:
    data = message.value
    count_per_second += 1      # 1초 단위로 카운터를 1씩 증가
    total_count += 1           # 전체 누적 카운트를 1씩 증가
    current_time = time.time() # 현재 시간 가져옴

    # 최근 1초동안 수신한 메세지 개수를 tps로 출력
    if current_time - start_time >= 1.0:
        print(
            f"현재 TPS={count_per_second} 건/초, "
            f"누적 수신={total_count} 건, "
            f"최근 force={data['force']}"
        )

        # 1초 단위 카운터를 다시 0으로 초기화
        count_per_second = 0
        # tps 측정 시작 시간을 현재 시간으로 갱신
        start_time = current_time