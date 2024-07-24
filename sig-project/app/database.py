import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # MySQL 사용자 이름
            password="admin",  # MySQL 비밀번호
            database="sig"  # 사용할 데이터베이스 이름
        )
        return connection
    except OSError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
mydb=get_db_connection()
cursor = mydb.cursor(dictionary=True)

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



            
def commit_db():
    conn=get_db_connection
    conn.commit()
    conn.close()

  
