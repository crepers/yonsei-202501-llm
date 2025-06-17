# agents/table_selector_agent/agent.py

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from ...tools.schema_tools import get_table_summaries

# 에이전트가 환경 변수를 사용할 수 있도록 .env 파일 로드
load_dotenv()

# 사용할 모델 이름을 환경 변수에서 가져옵니다.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# --- 동적으로 테이블 요약 정보 주입 ---
# 에이전트를 정의하기 전에, tools를 사용하여 현재 사용 가능한 테이블들의
# 가벼운 요약 정보를 불러옵니다.
TABLE_SUMMARIES = get_table_summaries()


# 테이블 선택을 전문으로 하는 에이전트
table_selector_agent = LlmAgent(
    name="TableSelectorAgent",
    
    model=MODEL_NAME,
    disallow_transfer_to_parent=False,
    instruction=f"""
You are a highly specialized agent. Your ONLY purpose is to select the most relevant tables to answer a user's query.

**CRITICAL INSTRUCTIONS:**
1.  Carefully analyze the user's question to understand their intent.
2.  Review the "AVAILABLE TABLE SUMMARIES" list provided below, which contains table names and their descriptions.
3.  Based on your analysis, identify the tables that are absolutely necessary to answer the question.
4.  Your output MUST BE a comma-separated list of the full table names that you have selected. For example: `your-project.your-dataset.table1`,`your-project.your-dataset.table2`
5.  If you think no tables are relevant to the user's question, or if the question is not about data, you MUST output the single word "NONE".
6.  Do not generate SQL. Do not answer the user's question. Do not add any explanation. Your sole output is the comma-separated list of table names or the word "NONE".

---
**AVAILABLE TABLE SUMMARIES:**

{TABLE_SUMMARIES}
---
"""
)