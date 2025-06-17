# sub_agents/execution_agent.py

from google.adk.agents import SequentialAgent
from ..query_planner.agent import query_planner_agent
from ..sql_validator.agent import sql_validator_agent
from ..bigquery_agent.agent import bigquery_agent
from ..insight_agent.agent import insight_agent

# SQL 생성부터 결과 분석까지의 실제 작업을 담당하는 순차 에이전트
execution_agent = SequentialAgent(
    name="ExecutionPipeline",
    description="A pipeline that takes a user query and selected table names, generates and validates SQL, executes it, and formats the result.",
    sub_agents=[
        query_planner_agent,
        sql_validator_agent,
        bigquery_agent,
        insight_agent,
    ]
)