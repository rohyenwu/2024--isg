import pandas as pd
import mysql.connector
from mysql.connector import Error
# csvRead/csvReadMain.py

import sys
import os
negative_csv_path = "/Users/iusong/Downloads/Negative2.csv"
positive_csv_path = "/Users/iusong/Downloads/Positive2.csv"
# 현재 디렉토리의 부모 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 이제 app.database를 import할 수 있습니다
from app import database
from database import insert_reviews, read_csv_with_header_skip
# 예시 함수 호출 (database.py에 있는 함수)
# 데이터프레임 읽기
negative_df = read_csv_with_header_skip(negative_csv_path, skip_header=False)
positive_df = read_csv_with_header_skip(positive_csv_path, skip_header=True)

# 데이터베이스에 리뷰 삽입
insert_reviews(negative_df, 'negative')
insert_reviews(positive_df, 'positive')


