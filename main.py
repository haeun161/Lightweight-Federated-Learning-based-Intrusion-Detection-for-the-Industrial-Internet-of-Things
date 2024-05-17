import pandas as pd
import numpy as np
import os  # os 모듈 추가
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras import optimizers
import psutil
import time

# 데이터셋 불러오기
dataset = pd.read_csv('./gitignore/dataset.csv', delimiter=',', low_memory=False)
dataset = dataset.select_dtypes(exclude=['object']) # object 형태 제외

# 데이터셋을 행별로 섞기
shuffled_dataset = dataset.sample(frac=1, random_state=42)

# 작업자 데이터셋 생성
num_workers = 3
worker_datasets = np.array_split(shuffled_dataset, num_workers)

# 모델 정의
def create_model():
    model = Sequential()
    model.add(Dense(10, input_shape=(48,), activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    return model

# 연합 학습을 위한 초기 모델 생성
global_model = create_model()

# 학습 파라미터 설정
learning_rate = 0.001
optimizer = optimizers.Adam(learning_rate)

# 연합 학습 반복 횟수 설정
num_epochs = 5

start1 = shuffled_dataset.columns.get_loc("detect_type(-)")
end1 = shuffled_dataset.columns.get_loc("ext(dll)") + 1
start2 = shuffled_dataset.columns.get_loc("label_tactic(1)")
end2 = shuffled_dataset.columns.get_loc("label_tactic(3)") + 1

# 모델 학습하기 전 메모리 사용량 측정 + 시간 start
memory_before = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB 단위로 변환
start_time = time.time()

# 연합 학습 실행
for epoch in range(num_epochs):
    worker_weights = []

    # 작업자별로 모델 학습 및 가중치 전송
    for i in range(num_workers):
        worker_dataset = worker_datasets[i]
        x_train = worker_dataset.iloc[1 + int(64278/5) * i : int(64278/5) * (i+1), start1:end1]
        y_train = worker_dataset.iloc[1 + int(64278/5) * i : int(64278/5) * (i+1), start2:end2]

        worker_model = create_model()
        worker_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        worker_model.fit(x_train, y_train, epochs=1, verbose=0)

        worker_weights.append(worker_model.get_weights())

    # 서버에서 가중치 평균 계산
    avg_weights = []
    for weights_list_tuple in zip(*worker_weights):
        avg_weights.append(np.mean(weights_list_tuple, axis=0))

    # 글로벌 모델에 평균 가중치 설정
    global_model.set_weights(avg_weights)

# 테스트 데이터 평가
x_test = shuffled_dataset.iloc[73500:, start1:end1]
y_test = shuffled_dataset.iloc[73500:, start2:end2]

global_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 학습 후 메모리 사용량 측정 + 시간 end
memory_after = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB 단위로 변환
end_time = time.time()
elapsed_time = end_time - start_time

# 모델 컴파일 후 테스트 데이터 평가
score = global_model.evaluate(x_test, y_test)
print('Accuracy: {}%'.format(score[1] * 100))

# 학습 중 사용된 메모리 계산
memory_used = memory_after - memory_before
print("Memory Usage: {} MB".format(memory_used))

#총 실행시간
elapsed_time = end_time - start_time
print("Latency: {:.2f}s".format(elapsed_time))