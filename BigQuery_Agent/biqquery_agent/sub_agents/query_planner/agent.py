# agents/query_planner/agent.py

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from ...tools.schema_tools import get_table_schemas # 스키마 로딩 도구 import

load_dotenv()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# 명확해진 질문과 스키마를 바탕으로 SQL을 생성하는 전문 에이전트
query_planner_agent = LlmAgent(
    name="QueryPlannerAgent",
    model=MODEL_NAME,
    tools=[get_table_schemas],
    disallow_transfer_to_parent=False,
    instruction=f"""
You are an expert SQL generation agent.
You will receive a JSON string input with "user_query" and "table_list".
First, use the `get_table_schemas` tool to get the detailed schema for the tables in "table_list".
Then, using the schema and the "user_query", generate the appropriate BigQuery SQL.

**CRITICAL:** Your final output MUST be a single JSON string with two keys:
1.  `status`: A string, set to "success".
2.  `sql_query`: A string, containing the generated SQL query.

Example: {{"status": "success", "sql_query": "SELECT * FROM ..."}}
"""
)


# You are an expert SQL generation agent for Google BigQuery.
# Your goal is to write a single, accurate, and efficient SQL query.

# **YOUR TASK:**
# 1.  You will receive a user's question and a comma-separated list of relevant table names.
# 2.  If the table list is "NONE", you must stop and output "Cannot generate SQL without table information.".
# 3.  If you have table names, your FIRST step is to use the `get_table_schemas` tool to retrieve the detailed schema for those specific tables.
# 4.  Using the retrieved schema and the original user's question, construct the final BigQuery SQL query.
# 5.  Your final output MUST BE ONLY the raw SQL query string. Do not add explanations or markdown formatting.
