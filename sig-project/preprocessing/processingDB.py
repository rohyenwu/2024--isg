from preDataBase import get_db_connection
from langdetect import detect


def preprocess_reviews():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 영어가 아닌 리뷰 삭제
        cursor.execute("SELECT review_id, review FROM reviews")
        reviews = cursor.fetchall()

        for review in reviews:
            try:
                if detect(review['review']) != 'en':
                    cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review['review_id'],))
            except:
                # 언어 감지 실패한 경우 무시
                continue

        conn.commit()

        # 리뷰가 없는 게임 삭제
        cursor.execute("""
            DELETE FROM game
            WHERE game_id NOT IN (SELECT DISTINCT game_id FROM reviews)
        """)

        conn.commit()

        # 리뷰가 100개 미만인 게임 삭제
        cursor.execute("""
            DELETE FROM game
            WHERE game_id IN (
                SELECT game_id
                FROM reviews
                GROUP BY game_id
                HAVING COUNT(*) < 100
            )
        """)

        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

preprocess_reviews()