# agents/sql_validator/agent.py

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from ...tools.bigquery_tools import validate_sql_with_dry_run # 도구 import

# 에이전트가 환경 변수를 사용할 수 있도록 로드합니다.
load_dotenv()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# 생성된 SQL을 사전 검증하는 전문 에이전트
sql_validator_agent = LlmAgent(
    name="SqlValidatorAgent",
    model=MODEL_NAME,
    tools=[validate_sql_with_dry_run],
    disallow_transfer_to_parent=False,
    instruction="""
You are a SQL validation agent.
You will receive a JSON string with a "sql_query".

**YOUR TASK:**
1.  Extract the "sql_query" from the input JSON.
2.  Use the `validate_sql_with_dry_run` tool to check this SQL.
3.  Your final output MUST be a JSON string that includes the original "sql_query" and the "validation_result".
    If validation fails, set "status" to "failure".

Example (Success): `{"status": "success", "sql_query": "SELECT ...", "validation_result": "Validation successful..."}`
Example (Failure): `{"status": "failure", "sql_query": "SELECT ...", "validation_result": "SQL Validation Failed..."}`
"""
)

# You are a specialized SQL validation agent.

# **YOUR TASK:**
# 1.  You will receive a single SQL query string as input.
# 2.  You MUST use the `validate_sql_with_dry_run` tool to check this SQL query.
# 3.  Your final output MUST be a single string that includes BOTH the original SQL query AND the validation result from the tool.

# **Example Output Format 1 (Success):**
# "SQL Query validated successfully. It will process approximately 2.15 MB of data.
# --- QUERY ---
# SELECT * FROM ..."

# **Example Output Format 2 (Failure):**
# "SQL Validation Failed. Error: Unrecognized name: activ at [1:50]
# --- QUERY ---
# SELECT * FROM ..."