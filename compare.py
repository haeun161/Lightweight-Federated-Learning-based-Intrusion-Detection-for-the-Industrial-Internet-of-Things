import pandas as pd
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import psutil
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#데이터셋 불러오기
dataset = pd.read_csv('./gitignore/dataset.csv', delimiter=',', low_memory=False)
dataset = dataset.select_dtypes(exclude=['object']) #object 형태 제외

# 데이터셋을 행별로 섞기 #데이터 수집시 sequential하게 수집했을 수도 있으므로
shuffled_dataset = dataset.sample(frac=1, random_state=42)  # frac=1은 전체 데이터셋을 선택, random_state는 재현성을 위한 랜덤 시드

# 작업자 데이터셋 생성
#데이터 범위 설정
start1 = shuffled_dataset.columns.get_loc("detect_type(-)")
end1 = shuffled_dataset.columns.get_loc("ext(dll)") + 1
start2 = shuffled_dataset.columns.get_loc("label_tactic(1)")
end2 = shuffled_dataset.columns.get_loc("label_tactic(3)") + 1

#training data: 전체 데이터셋의 대략 80% #test data: 전체 데이터셋의 대략 20%
x_train = shuffled_dataset.iloc[0:73500, start1:end1]
y_train = shuffled_dataset.iloc[0:73500, start2:end2]
x_test = shuffled_dataset.iloc[73500:, start1:end1]
y_test = shuffled_dataset.iloc[73500:, start2:end2]

#print("입력 데이터의 형태:", x_train.shape)
#print("출력 데이터의 형태:", y_train.shape)

# 모델 정의
model = Sequential()
model.add(Dense(10, input_shape=(48,), activation='relu')) #은닉층
model.add(Dense(5, activation='relu')) #은닉층
model.add(Dense(3, activation='softmax')) #출력층 #클래스 수에 해당하는 노드 수와 softmax 활성화 함수

# 모델 학습과정 설정
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'], run_eagerly=True)

# 모델 학습하기 전 메모리 사용량 측정
memory_before = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB 단위로 변환

# 연합 학습 실행
start_time = time.time()
model.fit(x_train, y_train, epochs=5, verbose=0)
end_time = time.time()
elapsed_time = end_time - start_time

# 모델 학습 후 메모리 사용량 측정
memory_after = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB 단위로 변환

# 평가
score = model.evaluate(x_test, y_test)
print('Accuracy: {}%'.format(score[1] * 100))

# 학습 중 사용된 메모리 계산
memory_used = memory_after - memory_before
print("Memory Usage: {} MB".format(memory_used))

#총 실행시간
elapsed_time = end_time - start_time
print("Latency: {:.2f}s".format(elapsed_time))