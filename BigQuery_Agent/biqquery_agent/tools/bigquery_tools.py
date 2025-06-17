# tools/bigquery_tools.py

import os
from google.cloud import bigquery
from google.cloud.exceptions import BadRequest
# from google.adk.tools import tool
import pandas as pd
import logging 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # 기본 로깅 레벨 설정

# @tool
def validate_sql_with_dry_run(sql: str) -> str:
    """
    입력된 SQL 쿼리를 BigQuery에서 실제로 실행하지 않고 'Dry Run'을 통해
    문법적 유효성과 예상 데이터 처리량을 확인합니다.
    `SqlValidatorAgent`가 사용합니다.
    """
    try:
        client = bigquery.Client(project=os.getenv("BIGQUERY_PROJECT"))
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
        
        # Dry run 쿼리 실행
        query_job = client.query(sql, job_config=job_config)

        # 예상 처리량 계산 (MB 단위)
        bytes_to_be_processed = query_job.total_bytes_processed
        megabytes = bytes_to_be_processed / (1024 * 1024) if bytes_to_be_processed else 0

        result= f"Validation successful. The query will process approximately {megabytes:.2f} MB of data."
        logger.info(result)
        
        return result


    except BadRequest as e:
        return f"SQL Validation Failed. Error: {e.message}"
    except Exception as e:
        return f"An unexpected error occurred during validation: {str(e)}"

# @tool
def execute_sql_query(sql: str) -> str:
    """
    검증이 완료된 SQL 쿼리를 BigQuery에서 실제로 실행하고,
    그 결과를 JSON 형식의 문자열로 반환합니다.
    `BigQueryExecutorAgent`가 사용합니다.
    """
    try:
        client = bigquery.Client(project=os.getenv("BIGQUERY_PROJECT"))
        
        # 쿼리 실행
        query_job = client.query(sql)
        
        # 결과를 Pandas DataFrame으로 변환
        df = query_job.to_dataframe()

        if df.empty:
            noResult = "Query executed successfully, but returned no results."
            logger.info(noResult)
            return noResult

        # DataFrame을 JSON 문자열로 변환
        result = df.to_json(orient="records")
        logger.info(result)
        
        return result
    

    except BadRequest as e:
        return f"SQL Execution Failed. Error: {e.message}"
    except Exception as e:
        return f"An unexpected error occurred during execution: {str(e)}"