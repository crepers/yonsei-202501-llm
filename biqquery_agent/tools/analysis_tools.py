# tools/analysis_tools.py

import pandas as pd
import json
import logging 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # 기본 로깅 레벨 설정

def convert_json_to_markdown(json_data: str) -> str:
    """
    JSON 형식의 데이터 문자열을 입력받아,
    사람이 읽기 좋은 마크다운(Markdown) 테이블 형식의 문자열로 변환합니다.
    `InsightGeneratorAgent`가 사용합니다.
    """
    # "no results" 같은 일반 텍스트는 그대로 반환
    if not json_data.strip().startswith('['):
        logger.info(f"convert_json_to_markdown - normal text: {json_data}")
        return json_data
        
    try:
        # JSON 문자열을 Pandas DataFrame으로 로드
        df = pd.read_json(json_data)
        
        if df.empty:
            return "The data is empty."
            
        # DataFrame을 마크다운 테이블로 변환 (인덱스 제외)
        output= df.to_markdown(index=False)
    
        logger.info(f"convert_json_to_markdown: {output}")
        return output

    except (json.JSONDecodeError, ValueError):
        logger.error(f"Could not format the following data into a table:\n{json_data}")
        return f"Could not format the following data into a table:\n{json_data}"
    except Exception as e:
        logger.error(f"An unexpected error occurred during data formatting: {str(e)}")
        return f"An unexpected error occurred during data formatting: {str(e)}"