# BigQuery Agent

사용자의 자연어 질문을 이해하고, Google BigQuery에서 관련 정보를 조회하여, 그 결과를 사용자에게 제공하는 AI 에이전트 시스템입니다.

## 🌟 주요 목표

- **자연어 이해:** 사용자의 복잡하고 모호할 수 있는 질문의 의도를 파악합니다.
- **동적 SQL 생성:** 여러 테이블의 스키마를 동적으로 파악하여 정확한 SQL 쿼리를 생성합니다.
- **안정적인 실행:** 생성된 SQL을 사전 검증하고 비용을 예측하여 안정성을 확보합니다.
- **통찰력 있는 결과:** 단순한 데이터 조회를 넘어, 결과를 분석하고 시각적으로 효과적인 형태로 가공하여 제공합니다.

---

## 🏛️ 아키텍처 (Architecture)

본 프로젝트는 **'지능형 라우터(Intelligent Router)' 패턴**을 따르는 멀티 에이전트 아키텍처로 구성됩니다. Root Agent가 지휘자 역할을 하며, 각 서브 에이전트는 '도구(Tool)'로서 호출됩니다.

**작업 흐름 (Workflow):**

1.  **[Root Agent]** 사용자의 모든 입력을 가장 먼저 받습니다.
2.  **[Clarification Tool 호출]** 질문이 불분명하거나 단순 인사말인지 판단합니다.
    -   만약 단순 인사/대화라면, 여기서 대화를 종료합니다.
    -   만약 질문이 모호하다면, 사용자에게 되묻고 대화를 종료합니다.
3.  **[Table Selector Tool 호출]** 명확해진 질문을 바탕으로 필요한 테이블을 선택합니다.
    -   만약 관련된 테이블이 없다면, 여기서 대화를 종료합니다.
4.  **[Execution Pipeline Tool 호출]** 명확한 질문과 선택된 테이블 목록을 가지고, 실제 데이터 처리 파이프라인을 실행합니다.
    -   (`Query Planner` -> `SQL Validator` -> `BigQuery Executor` -> `Insight Generator` 순차 실행)
5.  **[Root Agent]** 최종 결과를 사용자에게 전달합니다.

---

## 📁 프로젝트 구조 (Project Structure)

이 프로젝트는 ADK의 표준 'Agent App' 폴더 구조를 따릅니다.

```
BigQuery_Agent/
├── agents/                      # '전문가(Worker)' 에이전트들의 모음
│   ├── __init__.py
│   ├── bigquery_agent/          # SQL을 실제로 실행하는 에이전트
│   ├── clarification_agent/     # 사용자 질문의 모호성을 해소하는 에이전트
│   ├── execution_agent/         # SQL 실행 파이프라인 (SequentialAgent)
│   ├── insight_agent/           # 결과를 분석하고 최종 답변을 생성하는 에이전트
│   ├── query_planner/           # SQL을 생성하는 에이전트
│   ├── sql_validator/           # 생성된 SQL을 검증하는 에이전트
│   └── table_selector_agent/    # 필요한 테이블을 선택하는 에이전트
├── schemas/                     # 조회 가능한 테이블의 스키마 정보
│   ├── ..._schema.json
├── tools/                       # 에이전트들이 사용하는 도구의 실제 구현
│   ├── __init__.py
│   ├── analysis_tools.py        # 데이터 포맷팅 도구 (JSON -> Markdown)
│   ├── bigquery_tools.py        # BigQuery 연동 도구 (실행, 검증)
│   └── schema_tools.py          # 스키마 로딩 및 요약 도구
├── agent.py                     # [Root Agent] 전체 워크플로우를 조율하는 최상위 에이전트
├── __init__.py                  # 프로젝트를 파이썬 패키지로 인식
├── .env.example                 # 프로젝트에 필요한 환경 변수 예시
├── .gitignore                   # 버전 관리 제외 목록
├── requirements.txt             # 필요한 파이썬 라이브러리 목록
└── README.md                    # 프로젝트 설명 및 실행 방법 안내서
```

## 🚀 시작하기

### 사전 준비사항

- Python 3.9 이상
- Google Cloud SDK 설치 및 인증 (`gcloud auth application-default login`)

1. 가상 환경 생성 및 활성화

- Windows:
```
python -m venv venv && venv\Scripts\activate
```

- macOS / Linux: 
```
python3 -m venv venv && source venv/bin/activate
```

1. 필요 라이브러리 설치
```
# pip을 최신 버전으로 업그레이드
pip install --upgrade pip

# requirements.txt 파일로 모든 패키지 설치
pip install -r requirements.txt
```

1. 환경 변수 설정
.env.example 파일을 복사하여 .env 파일을 생성합니다.

`cp .env.example .env`

생성된 .env 파일을 열어, 주석을 참고하여 아래 항목들을 자신의 환경에 맞게 수정합니다.

- GOOGLE_CLOUD_PROJECT: AI 에이전트가 실행될 GCP 프로젝트 ID (Vertex AI 과금 주체)
- GOOGLE_CLOUD_LOCATION: Vertex AI 리전 (예: us-central1)
- BIGQUERY_PROJECT: 데이터가 저장된 BigQuery의 GCP 프로젝트 ID
- BIGQUERY_LOCATION: 데이터셋이 위치한 BigQuery 리전 (예: asia-northeast3 for Seoul)
- BIGQUERY_DATASET_ID: 조회할 데이터셋의 ID

1. 에이전트 실행 (로컬 테스트)
프로젝트 루트 디렉터리에서 adk web 명령어를 실행합니다.
`adk web`

브라우저에서 http://127.0.0.1:8000 주소로 접속하면 ADK 웹 UI가 나타나고, 바로 채팅을 시작할 수 있습니다.

## 💬 샘플 질문 (Sample Questions)
Show me the recommendation with the highest potential cost savings.
List all recommendations related to instance sizing.
What are the recommendations with a high impact score?
How many recommendations are currently in the ACTIVE state?
Show me recommendations targeted for the us-central1 region.
List the 10 most recent recommendations.
What recommendations are associated with the project 'my-gcp-project'?
Show recommendations that will expire within the next week.
List recommendations of type 'OPTIMIZE_SERVICE'.
What is the average potential cost savings across all recommendations?

What are the insight IDs of the 10 most recent insights?
How many insights are there for each resource project?
What is the average impact in terms of cost for all insights?
List the top 5 insight subtypes with the highest number of occurrences.
Show all insight resources of insight subtype 'google.compute.instance.IdleResourceAnalyzer'?
What are the insight IDs for insights with a high impact category?
How many insights are associated with each resource location?
What are the project IDs and insight IDs of insights with a severity of 'HIGH'?
Show the distribution of insights across different resource types.
What is the average CPU utilization reported in insights related to compute instances?