import pandas as pd
import mysql.connector
from mysql.connector import Error


# 데이터프레임 읽기 함수
def read_csv_with_header_skip(file_path, skip_header=False):
    try:
        df = pd.read_csv(file_path, encoding='utf-8', skiprows=1 if skip_header else 0)
        df.columns = df.columns.str.strip()  # 열 이름의 공백 제거
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
