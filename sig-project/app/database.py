import mysql.connector
from pydantic import BaseModel
from typing import Optional

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="172.30.125.249",
            user="sig2024",  # MySQL 사용자 이름
            password="sig2024",  # MySQL 비밀번호
            database="sig"  # 사용할 데이터베이스 이름
        )
        return connection
    except OSError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
class ReviewData(BaseModel):
    graphic: str
    sound: str
    story: str
    creativity: str
    graphicNative: str
    soundNative: str
    storyNative: str
    creativityNative: str
    graphicScore:float
    soundScore:float
    storyScore:float
    creativityScore:float
    
def get_summary_reviews(game_name: str) -> Optional[ReviewData]:
    mydb=get_db_connection()
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

        # 요약 리뷰를 ReviewData 형식으로 변환
        review_data = {
            "graphic": "",
            "sound": "",
            "story": "",
            "creativity": "",
            "graphicNative": "",
            "soundNative": "",
            "storyNative": "",
            "creativityNative": "",
            "graphicScore":"",
            "soundScore":"",
            "storyScore":"",
            "creativityScore":""
        }

        for review in summary_reviews:
            category_type = review["category_type"]
            polarity = review["summary_Polarity"]
            summary_review = review["summary_review"]

            if polarity == "positive":
                if category_type == "graphic":
                    review_data["graphic"] = summary_review
                elif category_type == "sound":
                    review_data["sound"] = summary_review
                elif category_type == "story":
                    review_data["story"] = summary_review
                elif category_type == "creativity":
                    review_data["creativity"] = summary_review
            elif polarity == "negative":
                if category_type == "graphic":
                    review_data["graphicNative"] = summary_review
                elif category_type == "sound":
                    review_data["soundNative"] = summary_review
                elif category_type == "story":
                    review_data["storyNative"] = summary_review
                elif category_type == "creativity":
                    review_data["creativityNative"] = summary_review
                    
        score_query="""
        SELECT s.score,c.category_type
        FROM score s
        JOIN category c ON s.category_id=c.category_id
        WHERE s.game_id=%s
        """
        cursor.execute(score_query, (game_id,))
        scores = cursor.fetchall()
        for score in scores:
            category_type = score["category_type"]
            score_value = score["score"]
            if category_type == "graphic":
                review_data["graphicScore"] = score_value
            elif category_type == "sound":
                review_data["soundScore"] = score_value
            elif category_type == "story":
                review_data["storyScore"] = score_value
            elif category_type == "creativity":
                review_data["creativityScore"] = score_value
        cursor.close()
        mydb.close()

        return ReviewData(**review_data)
    
    except Exception as e:
        print(f"Error fetching summary reviews for '{game_name}': {e}")
        return None

            
def commit_db():
    conn=get_db_connection
    conn.commit()
    conn.close()

  
