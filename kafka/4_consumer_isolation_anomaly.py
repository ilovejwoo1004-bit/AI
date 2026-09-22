# ================================================================
'''
Producer

     ↓

Kafka

press-force

     ↓

IsolationForest Consumer

     ↓

NORMAL 또는 ANOMALY   --> 결과 그래프 출력



part1_producer_10hz.py     (실행 1)
        ↓
part2_consumer_isolation.py  (실행 2)
'''

# ================================================================

# =====================================================
# Kafka Consumer
# =====================================================

# Kafka Topic 데이터를 읽기 위한 Consumer 클래스
from kafka import KafkaConsumer

# JSON 문자열 → Python Dictionary 변환
import json

import time

# 수치 계산
import numpy as np

# IsolationForest 이상탐지 모델
from sklearn.ensemble import IsolationForest

# 그래프
import matplotlib.pyplot as plt

# Ctrl+C 처리
import signal

# 프로그램 종료
import sys

# =====================================================
# Kafka Consumer 생성
# =====================================================

consumer = KafkaConsumer(

    # 구독 Topic
    "press-force",

    # Kafka Broker 주소
    bootstrap_servers="localhost:9092",

    # 최신 데이터부터 읽기
    auto_offset_reset="latest",

    # Consumer Group
    group_id="isolation-visual-group",

    # Kafka bytes → Dict 변환
    value_deserializer=lambda data:
    json.loads(data.decode("utf-8"))
)

# =====================================================
# 학습 설정
# =====================================================

# 초기 학습 데이터 개수
TRAIN_SIZE = 100 #50

# 학습 데이터 저장
train_data = []

# AI 모델
model = None

# =====================================================
# 결과 저장
# =====================================================

# 전체 Force 저장
all_force = []

# NORMAL / ANOMALY 저장
all_status = []

# 샘플 번호 저장
all_index = []

# =====================================================
# Threshold
# =====================================================

THRESHOLD = 170

# =====================================================
# 실시간 그래프 갱신 함수
# =====================================================

def update_graph():

    # 기존 그림 삭제
    ax.clear()

    # -----------------------------
    # Force 시계열
    # -----------------------------

    ax.plot(
        all_index,
        all_force,
        linewidth=2,
        color="blue",
        label="Force"
    )

    # -----------------------------
    # Threshold
    # -----------------------------

    ax.axhline(
        y=THRESHOLD,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Threshold={THRESHOLD}"
    )

    # -----------------------------
    # 이상 데이터 추출
    # -----------------------------

    anomaly_x = []

    anomaly_y = []

    for idx, force, status in zip(
        all_index,
        all_force,
        all_status
    ):

        if status == "ANOMALY":

            anomaly_x.append(idx)

            anomaly_y.append(force)

    # -----------------------------
    # 이상 데이터 표시
    # -----------------------------

    ax.scatter(
        anomaly_x,
        anomaly_y,
        color="red",
        s=100,
        marker="o",
        label="AI Anomaly"
    )

    # -----------------------------
    # 그래프 설정
    # -----------------------------

    ax.set_title(
        "Kafka + IsolationForest Anomaly Detection"
    )

    ax.set_xlabel(
        "Sample"
    )

    ax.set_ylabel(
        "Force"
    )

    ax.grid(True)

    ax.legend()

    plt.tight_layout()

    # 화면 강제 갱신
    fig.canvas.draw()

    fig.canvas.flush_events()

# =====================================================
# 최종 결과 시각화 함수
# =====================================================

def show_final_result():
    print("\n최종 결과 그래프 생성")

    plt.figure(
        figsize=(14, 7)
    )

    # -----------------------------
    # Force 시계열
    # -----------------------------

    plt.plot(
        all_index,
        all_force,
        linewidth=2,
        label="Force"
    )

    # -----------------------------
    # Threshold
    # -----------------------------

    plt.axhline(
        y=THRESHOLD,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Threshold={THRESHOLD}"
    )

    # -----------------------------
    # 이상 데이터 추출
    # -----------------------------

    anomaly_x = []

    anomaly_y = []

    for idx, force, status in zip(
        all_index,
        all_force,
        all_status
    ):

        if status == "ANOMALY":
            anomaly_x.append(idx)

            anomaly_y.append(force)

    # -----------------------------
    # 이상 데이터 표시
    # -----------------------------

    plt.scatter(
        anomaly_x,
        anomaly_y,
        color="red",
        s=100,
        marker="o",
        label="AI Anomaly"
    )

    # -----------------------------
    # 제목
    # -----------------------------

    plt.title(
        "Kafka + IsolationForest Anomaly Detection"
    )

    plt.xlabel(
        "Sample"
    )

    plt.ylabel(
        "Force"
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()



# =====================================================
# 실시간 그래프 설정
# =====================================================

# matplotlib 실시간 모드
plt.ion()

# 그래프 창 생성
fig, ax = plt.subplots(
    figsize=(14, 7)
)

# 그래프 갱신 주기 (10초)
UPDATE_INTERVAL = 10

# 마지막 갱신 시각
last_update_time = time.time()



# =====================================================
# Ctrl+C 처리
# =====================================================

def signal_handler(sig, frame):

    print("\n프로그램 종료")

    # 최종 그래프 한번 더 그림
    update_graph()

    # 실시간 모드 종료
    plt.ioff()

    # 최종 그래프 유지
    plt.show()

    sys.exit(0)


signal.signal(
    signal.SIGINT,
    signal_handler
)

# =====================================================
# 시작
# =====================================================

print(
    "IsolationForest Consumer 시작"
)

sample_no = 0

# =====================================================
# Kafka 데이터 수신
# =====================================================

for message in consumer:

    # Kafka 데이터
    data = message.value

    # 샘플 번호
    sample_no += 1

    # Force 값
    force = data["force"]

    # 저장
    all_index.append(sample_no)

    all_force.append(force)

    # AI 입력
    x = np.array([[force]])

    # ------------------------------------
    # 모델 학습 전
    # ------------------------------------

    if model is None:

        train_data.append([force])

        print(
            f"학습 데이터 수집중 "
            f"{len(train_data)}/{TRAIN_SIZE}"
        )

        # 100개 모이면 학습
        if len(train_data) >= TRAIN_SIZE:
            model = IsolationForest(

                contamination=0.05,

                random_state=42
            )

            model.fit(
                np.array(train_data)
            )

            print(
                "\nAI 모델 학습 완료\n"
            )

        continue

    # ------------------------------------
    # 예측
    # ------------------------------------

    pred = model.predict(x)

    # ------------------------------------
    # 결과 판정 (anomaly 판정 --> isolation -1 이상 / 1 정상)
    # ------------------------------------

    if pred[0] == -1:

        status = "ANOMALY"

    else:

        status = "NORMAL"

    # 결과 저장
    all_status.append(status)

    # ------------------------------------
    # 콘솔 출력
    # ------------------------------------

    print(
        f"Force={force:.2f}, "
        f"Result={status}"
    )

    # =====================================================
    # 10초마다 그래프 자동 갱신
    # =====================================================

    current_time = time.time()

    if current_time - last_update_time >= UPDATE_INTERVAL:
        print(
            "\n===== 그래프 갱신 =====\n"
        )

        update_graph()

        last_update_time = current_time