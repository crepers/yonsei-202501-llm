import os
from dotenv import load_dotenv

# from google.adk.agents import SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent

# 각 전문 에이전트를 해당 폴더의 agent.py 파일로부터 가져옵니다.
from .sub_agents.clarification_agent.agent import clarification_agent
from .sub_agents.table_selector_agent.agent import table_selector_agent
from .sub_agents.execution_agent.agent import execution_agent

load_dotenv()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ADK가 인식할 최종 Root Agent
root_agent = LlmAgent(
    name="BigQuery_Orchestrator",
    model=MODEL_NAME,
    tools=[
        AgentTool(clarification_agent),
        AgentTool(table_selector_agent),
        AgentTool(execution_agent),
    ],
    disallow_transfer_to_parent=False,
    instruction="""
You are a master orchestrator for a BigQuery data assistant. Your job is to manage a team of specialist agents (available as tools) to answer the user's question. You MUST follow a strict, step-by-step process.

**YOUR REQUIRED WORKFLOW:**

1.  **STEP 1: Clarify Intent.**
    - **Action:** Call the `ClarificationAgent` tool with the user's raw input.
    - **Analyze Result & Decide:** If the tool provides a final greeting or asks a question back to the user, STOP and return that as your final answer. Otherwise, use the output ('clarified_question') for the next step.

2.  **STEP 2: Select Tables.**
    - **Action:** Call the `TableSelectorAgent` tool with the 'clarified_question'.
    - **Analyze Result & Decide:** If the tool's output is "NONE", STOP and politely inform the user you cannot find relevant data. Otherwise, use the output ('selected_tables') for the next step.

3.  **STEP 3: Execute Data Pipeline.**
    - **Condition:** Only proceed if you have a 'clarified_question' from STEP 1 and a 'selected_tables' list from STEP 2.
    - **Action:** You MUST call the `ExecutionPipeline` tool.
    - **[CRITICAL] Input Formatting:** The input for the `ExecutionPipeline` tool MUST be a single JSON string. You must create this JSON string with two keys:
        - `user_query`: The value should be the 'clarified_question'.
        - `table_list`: The value should be the 'selected_tables' from the previous step.
        - Example: `{"user_query": "How many recommendations are currently in the ACTIVE state?", "table_list": "`your-project.your-dataset.recommendations`"}`
    - **Final Answer:** The output of the `ExecutionPipeline` tool is the final answer for the user.
"""
)