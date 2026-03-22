# data-mining-algorithms

데이터 마이닝의 핵심 알고리즘들을 직접 구현하며 학습한 프로젝트들을 정리한 저장소입니다.  
PySpark 기반 그래프 처리, 연관 규칙 마이닝, MinHash와 LSH를 활용한 문서 중복 탐지, TF-IDF 기반 문서 유사도 분석 등을 포함하고 있습니다.  
각 프로젝트를 통해 데이터 처리 과정, 알고리즘 설계 방식, 그리고 대규모 데이터 분석에서의 효율적인 계산 방법을 구현 중심으로 익혔습니다.

---

## Repository Overview

이 저장소는 데이터 마이닝과 대용량 데이터 처리의 핵심 개념을 직접 구현하며 학습한 프로젝트 모음입니다.  
단순히 이론을 정리하는 데 그치지 않고, 실제 입력 데이터를 읽고 전처리한 뒤, 알고리즘을 적용하여 결과를 출력하는 전체 과정을 Python 코드로 구현했습니다.

주요 주제는 다음과 같습니다.

- PySpark를 활용한 그래프 분석
- Association Rule Mining
- MinHash + LSH 기반 near-duplicate document detection
- TF-IDF + Random Projection 기반 document similarity analysis

---
## Projects

### 1. Spark Graph Square Detection

**File:** `src/spark_graph_square_detection.py`

#### 개요
소셜 그래프 형태의 입력 데이터를 읽어, 상호 연결된 관계만을 이용해 무방향 그래프를 구성한 뒤, 그래프 내부의 square 구조(4-cycle)를 탐지하는 프로젝트입니다.

#### 구현 내용
- 인접 리스트 형식의 그래프 데이터 파싱
- directed edge를 mutual relation 기준으로 filtering하여 undirected edge 생성
- 공통 이웃 정보를 바탕으로 square 후보 탐색
- 중복 제거 후 사전식 순서 기준으로 결과 출력

#### 배운 점
- Spark의 RDD 기반 연산 흐름을 실제 문제에 적용하는 방법
- `flatMap`, `reduceByKey`, `groupByKey`, `distinct`, `broadcast` 같은 핵심 연산의 사용 방식
- 그래프 문제를 분산 처리 환경에서 어떻게 설계해야 하는지에 대한 이해
- 단순 brute force 대신 구조적 조건을 이용해 탐색 범위를 줄이는 방법

---

### 2. Association Rule Mining

**File:** `src/association_rule_mining.py`

#### 개요
장바구니 형태의 트랜잭션 데이터로부터 frequent item, frequent pair, 그리고 confidence 기준의 association rule을 추출하는 프로젝트입니다.

#### 구현 내용
- 전체 아이템의 출현 빈도 계산
- minimum support threshold를 만족하는 frequent item 선별
- triangular indexing을 이용한 frequent pair counting
- pair support를 기반으로 association rule 생성
- confidence 기준 정렬 후 상위 rule 출력

#### 배운 점
- support와 confidence의 의미를 실제 코드로 구현하며 이해
- 연관 규칙 분석의 전체 파이프라인을 직접 구성한 경험
- pair counting 과정에서 메모리를 절약하기 위한 triangular indexing 기법 이해
- 데이터 마이닝에서 효율적인 자료구조 선택이 얼마나 중요한지 학습

---

### 3. Near-Duplicate Document Detection with MinHash + LSH

**File:** `src/minhash_lsh_near_duplicate_detection.py`

#### 개요
문서를 정규화한 뒤 3-shingle 집합으로 변환하고, MinHash signature와 LSH를 이용해 유사 문서 후보를 효율적으로 탐지하는 프로젝트입니다.

#### 구현 내용
- 텍스트 정규화 및 알파벳/공백 기준 전처리
- 3-shingle 생성
- MinHash signature 계산
- banding 기법을 활용한 LSH bucket 구성
- candidate pair 생성 및 유사 문서 출력

#### 배운 점
- Jaccard similarity를 직접 계산하지 않고도 근사적으로 유사도를 비교하는 방법
- MinHash가 왜 set similarity 문제에 적합한지에 대한 이해
- LSH가 전체 pairwise comparison 비용을 줄이는 원리 학습
- 정확도와 계산 효율 사이의 trade-off를 구현 관점에서 경험

---

### 4. Document Similarity with TF-IDF + Random Projection

**File:** `src/tfidf_random_projection_similarity.py`

#### 개요
문서를 토큰 단위로 전처리한 뒤 TF-IDF 벡터를 구성하고, random projection signature와 cosine similarity를 이용해 유사 문서를 찾는 프로젝트입니다.

#### 구현 내용
- 텍스트 정규화 및 토큰화
- term frequency / document frequency 계산
- TF-IDF 벡터 생성
- random projection 기반 binary signature 생성
- bucket 기반 candidate pair 생성
- cosine similarity를 통한 최종 유사도 검증

#### 배운 점
- TF-IDF가 문서를 수치 벡터로 표현하는 방식 이해
- cosine similarity가 문서 유사도 비교에 어떻게 사용되는지 학습
- 고차원 벡터를 더 간단한 signature로 압축하는 아이디어 경험
- exact similarity 계산과 approximate search의 차이 이해

---

## Skills Demonstrated

- Python
- PySpark
- NumPy
- Data Mining
- Graph Processing
- Association Rule Mining
- Text Preprocessing
- Shingling
- MinHash
- Locality-Sensitive Hashing (LSH)
- TF-IDF
- Cosine Similarity
- Random Projection
- Algorithm Implementation
