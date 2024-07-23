import pandas as pd
import mysql.connector
from mysql.connector import Error

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

# 데이터베이스 연결
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='yourdatabase',
            user='root',
            password='newpassword123'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# 데이터베이스 연결
conn = create_connection()
if conn is None:
    exit()

cursor = conn.cursor()

# 게임을 데이터베이스에 삽입하고 게임 ID를 반환하는 함수
def get_or_insert_game(game_name):
    cursor.execute("SELECT game_id FROM game WHERE game_name = %s", (game_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO game (game_name) VALUES (%s)", (game_name,))
        conn.commit()
        return cursor.lastrowid

# 데이터베이스에 삽입하기 전에 NaN 값을 처리하는 함수
def clean_data(df):
    df = df.fillna('')  # NaN을 빈 문자열로 대체
    return df

# 리뷰 데이터 삽입 함수
def insert_reviews(df, polarity):
    if df is not None:
        df = clean_data(df)  # NaN 값 처리
        for _, row in df.iterrows():
            game_name = row['Game Name']
            user_name = row['User Name']
            review_text = row['Review Text']

            # 게임을 데이터베이스에 삽입하고 게임 ID를 얻기
            game_id = get_or_insert_game(game_name)

            # 리뷰 삽입
            cursor.execute("INSERT INTO reviews (review, game_id, review_polarity) VALUES (%s, %s, %s)", 
                           (review_text, game_id, polarity))

        conn.commit()
        print(f"Inserted {len(df)} reviews into the 'reviews' table with polarity '{polarity}'.")

# 데이터프레임 읽기
negative_df = read_csv_with_header_skip(negative_csv_path, skip_header=False)
positive_df = read_csv_with_header_skip(positive_csv_path, skip_header=True)

# 데이터베이스에 리뷰 삽입
insert_reviews(negative_df, 'negative')
insert_reviews(positive_df, 'positive')

# 연결 닫기
cursor.close()
conn.close()
