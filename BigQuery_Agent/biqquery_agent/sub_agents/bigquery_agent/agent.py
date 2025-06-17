# agents/bigquery_agent/agent.py

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from ...tools.bigquery_tools import execute_sql_query # 도구 import

# 에이전트가 환경 변수를 사용할 수 있도록 로드합니다.
load_dotenv()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# BigQuery 쿼리 실행 전문 에이전트
bigquery_agent = LlmAgent(
    name="BigQueryExecutorAgent",
    model=MODEL_NAME,
    tools=[execute_sql_query], # 도구 연결
    instruction="""
You are a BigQuery execution agent.
You will receive a JSON string.

**YOUR TASK:**
1.  Check the "status" key in the input JSON. If it is "failure", you must pass the entire original JSON string through as your output without change.
2.  If the status is "success", extract the "sql_query".
3.  Use the `execute_sql_query` tool to run the SQL.
4.  Your final output MUST be a JSON string including the original "sql_query" and the "execution_result" (which is the data as a JSON string, or an error message). Update the "status" based on the tool's result.

Example: `{"status": "success", "sql_query": "SELECT ...", "execution_result": "[{\\"col\\":\\"val\\"}]"}`
"""
)

# You are a BigQuery execution agent.
# Your ONLY job is to execute the SQL query provided to you.
# You MUST use the 'execute_sql_query' tool to run the input SQL.
# Do not modify the SQL query.
# Do not analyze the query.
# Simply execute the query using the available tool and return the result as a JSON string.