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

# 리뷰 데이터 삽입 함수
def insert_reviews(df, polarity):
    conn=get_db_connection()
    cursor=conn.cursor()
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
        # 연결 닫기
    cursor.close()
    conn.close()
# 데이터베이스에서 카테고리 ID를 가져오는 함수
def get_category_id(category_type):
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT category_id FROM category WHERE category_type = %s", (category_type,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"Category '{category_type}' not found.")
        return None
# 게임을 데이터베이스에 삽입하고 게임 ID를 반환하는 함수
def get_or_insert_game(game_name):
    conn=get_db_connection()
    cursor=conn.cursor()
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

def fetch_reviews():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT game_id, review FROM game_reviews")
    return cursor.fetchall()

def fetch_Negative_reviews():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT game_id, review FROM game_reviews WHERE review_Polarity = 'positive' ")
    return cursor.fetchall()

def fetch_Positive_reviews():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT game_id, review FROM game_reviews WHERE review_Polarity = 'negative' ")
    return cursor.fetchall()

#키워드 추출 데이터베이스에 넣을 수 있는 형식으로 바꾸기
def convert_keywordstype(data):
    keyWords = []
    for category, words in data.items():
        for word in words:
            keyWords.append((category, word))
    return keyWords

# 키워드를 데이터베이스에 저장하는 함수
def store_keywords(keyWords):
    conn=get_db_connection()
    cursor=conn.cursor()
    for category, similar_word in keyWords:
        category_id = get_category_id(cursor, category)
        if category_id is not None:
            cursor.execute(
                "INSERT INTO word (similar_word, category_id) VALUES (%s, %s)",
                (similar_word, category_id)
            )

# # 요약된 리뷰를 데이터베이스에 저장하는 함수
def store_summaries(cursor, gameID, pGraphic, pSound, pStory, pCreativity, nGraphic, nSound, nStory, nCreativity):
    # 긍정적인 리뷰를 삽입
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (pGraphic, gameID, 1, 'Positive')
    )
    
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (pSound, gameID, 2, 'Positive')
    )
    
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (pStory, gameID, 3, 'Positive')
    )
    
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (pCreativity, gameID, 4, 'Positive')
    )
    
    # 부정적인 리뷰를 삽입
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (nGraphic, gameID, 1, 'Negative')
    )
    
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (nSound, gameID, 2, 'Negative')
    )
    
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (nStory, gameID, 3, 'Negative')
    )
    
    cursor.execute(
        "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)",
        (nCreativity, gameID, 4, 'Negative')
    )
