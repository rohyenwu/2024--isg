import pandas as pd
import mysql.connector
from mysql.connector import Error
from preDataBase import get_db_connection, get_or_insert_game, insert_reviews
# CSV 파일 경로 설정
negative_csv_path = "/Users/iusong/Downloads/Negative2.csv"
positive_csv_path = "/Users/iusong/Downloads/Positive2.csv"

# 데이터프레임 읽기 함수
def read_csv_with_header_skip(file_path, skip_header=False):
    try:
        df = pd.read_csv(file_path, encoding='utf-8', skiprows=1 if skip_header else 0)
        df.columns = df.columns.str.strip()  # 열 이름의 공백 제거
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# 데이터프레임 읽기
negative_df = read_csv_with_header_skip(negative_csv_path, skip_header=False)
positive_df = read_csv_with_header_skip(positive_csv_path, skip_header=True)

# 데이터베이스에 리뷰 삽입
insert_reviews(negative_df, 'negative')
insert_reviews(positive_df, 'positive')


