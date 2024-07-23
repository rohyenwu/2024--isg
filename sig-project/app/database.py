import mysql.connector
from crawling import crawling
from summarize import summarize_reviews
import csv

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            ##user="yourusername",  # MySQL 사용자 이름
            ##password="yourpassword",  # MySQL 비밀번호
            ##database="yourdatabase"  # 사용할 데이터베이스 이름
        )
        return connection
    except OSError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
mydb=get_db_connection()

def get_summary_reviews(game_name):
    cursor = mydb.cursor(dictionary=True)
    
    try:
        # 게임 이름으로 게임 ID 조회
        game_id_query = "SELECT game_id FROM game WHERE game_name = %s"
        cursor.execute(game_id_query, (game_name,))
        game = cursor.fetchone()
        
        if not game:
        
            return None
        
        game_id = game['game_id']
        
        # 게임 ID로 요약 리뷰 조회
        summary_review_query = """
        SELECT sr.summary_review, sr.summary_Polarity, c.category_type
        FROM summary_review sr
        JOIN category c ON sr.category_id = c.category_id
        WHERE sr.game_id = %s
        """
        cursor.execute(summary_review_query, (game_id,))
        summary_reviews = cursor.fetchall()
        
        if not summary_reviews:
            print(f"게임 '{game_name}'에 대한 요약 리뷰가 없습니다.")
            return None
        

        cursor.close()
        mydb.close()
        
        return summary_reviews
    
    except Exception as e:
        print(f"Error fetching summary reviews for '{game_name}': {e}")
        return None


def read_csv_to_flat_dict(file_path):
    reviews = []
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)

        # Print the field names to debug
        print("CSV Headers:", csv_reader.fieldnames)
        
        for row in csv_reader:
            reviews.append({
                'game_name': row['Game Name'],
                'user_name': row['User Name'],
                'review_text': row['Review Text']
            })
    return reviews

def Positive_reviews_insert_db():
    file_path = '파일 경로 설정'  # 파일 경로를 설정합니다.
    
    # CSV 파일에서 데이터를 읽어옵니다
    game_review_data = read_csv_to_flat_dict(file_path)
    
    # 데이터베이스 커서 생성 (이미 연결된 상태라고 가정)
    cursor = mydb.cursor(dictionary=True)

    try:
        # 게임 이름과 리뷰를 삽입합니다
        game_ids = {}  # 게임 이름에 대한 ID를 저장하는 딕셔너리

        for review in game_review_data:
            game_name = review['game_name']
            user_name = review['user_name']
            review_text = review['review_text']
            polarity = "positive"  # 예를 들어, 'positive', 'negative', 'neutral' 등의 값

            # 게임 이름에 대한 ID를 확인하거나 새로 삽입합니다
            if game_name not in game_ids:
                cursor.execute("SELECT id FROM games WHERE game_name = %s", (game_name,))
                result = cursor.fetchone()
                
                if result:
                    game_id = result['id']
                else:
                    cursor.execute("INSERT INTO games (game_name) VALUES (%s)", (game_name,))
                    game_id = cursor.lastrowid  # 자동 증가된 game_id를 가져옵니다
                
                game_ids[game_name] = game_id

            # 게임 리뷰를 삽입합니다
            cursor.execute(
                "INSERT INTO game_reviews (game_id, user_name, review, polarity) VALUES (%s, %s, %s, %s)",
                (game_ids[game_name], user_name, review_text, polarity)
            )
        
        # 모든 변경 사항을 커밋합니다
        mydb.commit()
    except Exception as e:
        print("An error occurred:", e)
        mydb.rollback()  # 오류 발생 시 롤백
    finally:
        cursor.close()
        
def Negative_reviews_insert_db():
    file_path='파일 경로 설정'
    #csv 파일 읽어서 딕셔너리로 만드는 코드 필요
    game_review_data=read_csv_to_dict(file_path)
    cursor = mydb.cursor(dictionary=True)

        # 데이터베이스에 데이터 삽입
        # 1. 게임 이름을 먼저 삽입
    for game in game_review_data:
        game_name = game['game_name']
            
        cursor.execute("INSERT INTO game (game_name) VALUES (%s)", (game_name,))
        game_id = cursor.lastrowid  # 방금 삽입된 game_id를 가져옵니다
            
    for review in game['reviews']:
                user_name = review['user_name']
                review_text = review['review_text']
                polarity = "negative"  # 예를 들어, 'positive', 'negative', 'neutral' 등의 값

                # 게임 리뷰 삽입
                cursor.execute(
                    "INSERT INTO game_reviews (game_id, review, polarity) VALUES (%s, %s, %s)",
                    (game_id, review_text, polarity)
                )



# 데이터베이스에서 카테고리 ID를 가져오는 함수
def get_category_id(category_type):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT category_id FROM category WHERE category_type = %s", (category_type,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"Category '{category_type}' not found.")
        return None

def fetch_reviews(cursor):
    cursor.execute("SELECT game_id, review FROM game_reviews")
    return cursor.fetchall()

# 키워드를 데이터베이스에 저장하는 함수
def store_keywords(cursor, keyWords):
    for category, similar_word in keyWords:
        category_id = get_category_id(cursor, category)
        if category_id is not None:
            cursor.execute(
                "INSERT INTO word (similar_word, category_id) VALUES (%s, %s)",
                (similar_word, category_id)
            )

# 요약된 리뷰를 데이터베이스에 저장하는 함수
def store_summaries(cursor, pGraphic, pSound, pStory, pCreativity, nGraphic, nSound, nStory, nCreativity):
    for game_id, categories in reviews_by_game_and_category.items():
        for category_id, reviews in categories.items():
            summary = summarize_reviews(reviews)
            cursor.execute(
                "INSERT INTO summury_review (summury_review, game_id, category_id) VALUES (%s, %s, %s)",
                (summary, game_id, category_id)
            )

            
def commit_db():
    conn=get_db_connection
    conn.commit()
    conn.close()

  
