# Kafka Consumer
from kafka import KafkaConsumer

# JSON 처리
import json

# 그래프
import matplotlib.pyplot as plt

# 시간 측정
import time

# 데이터 저장
from collections import deque


# Kafka Consumer 생성
consumer = KafkaConsumer(

    "press-force",

    bootstrap_servers="localhost:9092",

    auto_offset_reset="latest",

    group_id="graph-consumer-group",

    value_deserializer=lambda data:
    json.loads(data.decode("utf-8"))
)


# 최근 1000개 데이터 저장
MAX_POINTS = 1000

x_data = deque(maxlen=MAX_POINTS)

force_data = deque(maxlen=MAX_POINTS)


# 실시간 모드
plt.ion()

fig, ax = plt.subplots(figsize=(12, 6))

line, = ax.plot([], [], linewidth=2)

ax.set_title(
    "Real-Time Press Force Monitoring"
)

ax.set_xlabel("Sample")

ax.set_ylabel("Force")

ax.grid(True)


# 샘플 번호
sample_no = 0


# 마지막 그래프 갱신 시간
last_update_time = time.time()


# 5초
UPDATE_INTERVAL = 5


print(
    "5초 단위 그래프 업데이트 시작"
)


for message in consumer:

    # 데이터 수신
    data = message.value

    sample_no += 1

    force = data["force"]

    x_data.append(sample_no)

    force_data.append(force)

    print(
        f"수신 Sample={sample_no}, "
        f"Force={force}"
    )

    # 현재 시간
    current_time = time.time()

    # 20초가 지났는지 확인
    if current_time - last_update_time >= UPDATE_INTERVAL:

        print(
            "\n======================"
        )

        print(
            f"{UPDATE_INTERVAL}초 데이터 수집 완료"
        )

        print(
            f"총 데이터 수 : {len(force_data)}"
        )

        print(
            "그래프 업데이트"
        )

        print(
            "======================\n"
        )

        # 그래프 갱신
        line.set_data(
            list(x_data),
            list(force_data)
        )

        # X축 범위
        ax.set_xlim(
            min(x_data),
            max(x_data)
        )

        # Y축 범위 자동 조정
        ax.set_ylim(
            min(force_data) - 10,
            max(force_data) + 10
        )

        # 다시 그림
        fig.canvas.draw()

        fig.canvas.flush_events()

        # 다음 5초 측정
        last_update_time = current_time