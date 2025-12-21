# P02 프로젝트: 리만 제타 함수 시각화 및 시뮬레이션

## 프로젝트 개요

P02 프로젝트는 리만 제타 함수(Riemann Zeta Function)의 비자명 영점(non-trivial zeros)에 대한 시각화 및 시뮬레이션을 수행하는 프로젝트입니다. 

P01 프로젝트에서 다룬 소수 분포와 리만 가설 연구를 기반으로, 리만 제타 함수의 영점들이 가지는 수학적 특성과 물리적 의미를 탐구합니다.

## 프로젝트 구조

```
P02/
├── data/              # 데이터 파일
├── log/               # 로그 파일
│   ├── chat log/      # 채팅 로그
│   └── job log/       # 작업 로그
├── plan/              # 계획 문서
├── report/            # 분석 보고서
├── script/            # Python 스크립트
│   ├── 1.py          # 리만 제타 함수 시뮬레이션 (비가환 소음)
│   ├── 2.py          # 에너지 지형 시각화
│   ├── 3.py          # 입자 시뮬레이션
│   ├── 4.py          # 벡터장 시각화
│   ├── 5.py          # 쿨롱 가스 시뮬레이션
│   ├── 7.py          # 영점 예측
│   └── 8.py          # 제타 벨 소리 생성
└── README.md          # 본 파일

```

## 주요 스크립트 설명

### 1.py - 리만 제타 함수 시뮬레이션
비가환 소음(non-commutative noise)을 적용한 리만 제타 함수의 근사값 계산 및 시각화. 리만의 세계(질서)와 불확정 군의 세계(혼돈)를 비교 분석.

### 2.py - 에너지 지형 시각화
복소평면 상의 에너지 지형을 계산하여 영점의 안정성을 분석. 질서 에너지와 혼돈 에너지의 합으로 시스템 에너지를 계산.

### 3.py - 입자 시뮬레이션
에너지 함수의 기울기를 따라 이동하는 입자들의 진화 과정을 시뮬레이션. 영점 근처로 수렴하는 입자들의 궤적을 시각화.

### 4.py - 벡터장 시각화
에너지 기울기에 따른 벡터장(유동장)을 계산하여 영점이 '싱크(Sink)'로 작용하는 흐름을 시각화.

### 5.py - 쿨롱 가스 시뮬레이션
영점들 간의 척력(repulsion)을 시뮬레이션하여 중근(multiple roots)이 불가능한 이유를 물리적으로 설명.

### 7.py - 영점 예측
거시적 예측(통계)과 미시적 예측(물리)을 결합하여 다음 영점의 위치를 예측하는 모델.

### 8.py - 제타 벨 소리 생성
리만 제타 함수의 영점들을 주파수로 변환하여 소리로 합성. 비가환적 화음을 생성.

## 의존성

주요 Python 패키지:
- numpy
- matplotlib
- scipy

자세한 내용은 `requirements.txt`를 참조하세요.

## 사용 방법

1. 가상환경 생성 및 활성화:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 스크립트 실행:
```bash
python script/1.py
```

## 관련 프로젝트

- **P01**: 소수 분포 분석 및 리만 가설 연구

## 참고 문헌

- Riemann, B. (1859): "Über die Anzahl der Primzahlen unter einer gegebenen Größe"
- Edwards, H. M. (2001): "Riemann's Zeta Function"
- Davenport, H. (2000): "Multiplicative Number Theory"

## 라이선스

이 프로젝트는 연구 및 교육 목적으로 작성되었습니다.

