# tools/schema_tools.py

import os
import yaml  # json 대신 yaml 라이브러리 사용
from pathlib import Path
from typing import List, Dict, Any
import logging 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # 기본 로깅 레벨 설정

def _get_all_schemas_from_yaml_files() -> Dict[str, Any]:
    """
    (Helper Function) 'schemas/' 디렉터리에서 모든 스키마(.yaml)를 읽어와
    순수 테이블 이름을 key로 하는 딕셔너리로 반환합니다.
    """
    # 현재 파일의 위치를 기준으로 schemas 폴더 경로를 정확히 찾습니다.
    schema_dir = Path(__file__).parent.parent / "schemas"
    all_schemas = {}
    if not schema_dir.is_dir():
        print(f"Warning: Schema directory not found at {schema_dir}")
        return all_schemas

    # .yaml 또는 .yml 확장자를 가진 모든 파일을 찾습니다.
    for schema_file in schema_dir.glob("*.y*ml"):
        with open(schema_file, "r", encoding="utf-8") as f:
            try:
                schema_content = yaml.safe_load(f)
                # YAML 파일 상단에 정의된 table_name을 사용합니다.
                table_name = schema_content.get("table_name")
                if table_name:
                    all_schemas[table_name] = schema_content
            except yaml.YAMLError as e:
                print(f"Warning: Error parsing YAML file {schema_file}: {e}")
    return all_schemas

def get_table_summaries() -> str:
    """
    사용 가능한 모든 테이블의 이름과 설명을 요약하여 반환합니다.
    """
    project_id = os.getenv("BIGQUERY_PROJECT")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    all_schemas = _get_all_schemas_from_yaml_files()

    if not all_schemas:
        return "No table summaries found."

    summaries = []
    for table_name, schema in all_schemas.items():
        full_table_name = f"`{project_id}.{dataset_id}.{table_name}`"
        # YAML 구조에 맞게 description을 찾습니다. 여기서는 예시로 최상위를 가정합니다.
        table_desc = schema.get("description", "A table containing system data.")
        summaries.append(f"- Table Name: {full_table_name}\n  Description: {table_desc}")
    
    return "You can use the following tables:\n\n" + "\n".join(summaries)

def get_table_schemas(table_list_str: str) -> str:
    """
    쉼표로 구분된 전체 테이블 이름 문자열을 입력받아,
    각 테이블에 해당하는 상세 스키마 정보를 포맷팅하여 반환합니다.
    """
    if not table_list_str or table_list_str.upper() == "NONE":
        return "Error: No tables were provided to retrieve schemas for."

    try:
        table_names = [name.split('.')[-1].replace('`', '') for name in table_list_str.split(',')]
    except Exception:
        return f"Error: Could not parse the provided table list: {table_list_str}"

    all_schemas_map = _get_all_schemas_from_yaml_files()
    project_id = os.getenv("BIGQUERY_PROJECT")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")

    found_schemas = []
    for table_name in table_names:
        if table_name in all_schemas_map:
            schema = all_schemas_map[table_name]
            full_table_name = f"`{project_id}.{dataset_id}.{table_name}`"
            # YAML의 중첩 구조 'schema.fields'에서 컬럼 정보를 가져옵니다.
            fields = schema.get("schema", {}).get("fields", [])
            
            columns_str_list = []
            for col in fields:
                col_name = col.get("name")
                col_type = col.get("type")
                # RECORD 타입의 경우, 중첩되었다는 정보만 알려주는 것이 LLM에게 더 효과적일 수 있습니다.
                if col_type == 'RECORD':
                    col_desc = f"{col.get('description', '').strip()} (This is a nested field)."
                else:
                    col_desc = col.get('description', '').strip().replace('\n', ' ')
                
                columns_str_list.append(f"  - `{col_name}` ({col_type}): {col_desc}")

            columns_str = "\n".join(columns_str_list)
            
            schema_info = f"Table Name: {full_table_name}\nColumns:\n{columns_str}"
            found_schemas.append(schema_info)

    if not found_schemas:
        return f"Error: No matching schemas found for the tables: {table_names}"

    return "You MUST use the following table schemas to generate the SQL query:\n\n" + "\n\n---\n\n".join(found_schemas)