# agents/insight_agent/agent.py

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from ...tools.analysis_tools import convert_json_to_markdown # 도구 import

# 에이전트가 환경 변수를 사용할 수 있도록 로드합니다.
load_dotenv()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# 조회된 데이터를 분석하고 사용자 친화적으로 가공하는 전문 에이전트
# insight_agent = LlmAgent(
#     name="InsightGeneratorAgent",
#     model=MODEL_NAME,
#     tools=[convert_json_to_markdown], # 도구 연결
#     instruction="""
# You are an output formatting robot. Your ONLY function is to take an input JSON object and construct a final report by filling in a predefined template. You MUST follow the template structure precisely.

# You will receive a single JSON string as input. This JSON will contain the keys: "status", "sql_query", and "execution_result".

# **CRITICAL INSTRUCTIONS FOR SUCCESSFUL OPERATION:**

# 1.  **FAILURE CHECK:** If the "status" key in the input JSON has a value of "failure", you MUST IGNORE the template. Your only output should be a single string: "An error occurred with the query: `[The value of the 'sql_query' key]`. Details: [The value of the 'execution_result' key]".

# 2.  **SUCCESS TEMPLATE:** If the "status" is "success", your output MUST be a single block of text created by filling the template below.

# **--- FINAL OUTPUT TEMPLATE (FILL THIS OUT) ---**

# **Query Details**
# This result was generated using the following SQL query:
# ```sql
# [Directly insert the value of the "sql_query" key from the input JSON here.]
# ```

# **Summary**
# [Directly write a one-sentence, objective summary of the data found in the "execution_result" key here.]

# **Data**
# [Directly call the `convert_json_to_markdown` tool with the "execution_result" value and place the tool's output here.]

# **--- END OF TEMPLATE ---**

# Do not add any introductory or concluding text outside of this template. Your response must start with "**Query Details**".
# """
# )

insight_agent = LlmAgent(
    name="InsightGeneratorAgent",
    model=MODEL_NAME,
    # tools=[convert_json_to_markdown], # 도구 연결
    instruction="""
You are a data analyst agent. Your goal is to provide clear and insightful answers to the user.
You will receive a single JSON string as input. This JSON will contain the keys: "status", "sql_query", and "execution_result".
Follow these steps to create your response:

1.  **Summarize:** Start with a brief, one or two-sentence summary of the key findings in the data found in the "execution_result" key here. Speak in a friendly, helpful tone.
2.  **Present Data:** After the summary, present the detailed data as a Markdown table with the "execution_result" value. Ensure the table is well-formatted. Do not include the index column.

Example Response Format:
I found 5 security recommendations for you from the last week. Here are the details:

Query: [Directly insert the value of the "sql_query" key from the input JSON here.]

---

| recommender_subtype | description                               |
|---------------------|-------------------------------------------|
| SECURITY            | Enable IAM recommendations for project... |
| SECURITY            | Restrict API keys for project...          |

Your final output should be a single block of text containing the summary and the Markdown table.
"""
)