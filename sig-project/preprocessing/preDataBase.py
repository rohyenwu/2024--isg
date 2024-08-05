import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='yourdatabase',
            user='root',
            password='newpassword123'
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
        return result['category_id']
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
    cursor.execute("SELECT review FROM reviews") #테이블 이름 수정및 게임 id삭제
    return cursor.fetchall()

def fetch_Negative_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT game_id, review FROM reviews WHERE review_polarity = 'negative'")
    return cursor.fetchall()

def fetch_Positive_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT game_id, review FROM reviews WHERE review_polarity = 'positive'")
    return cursor.fetchall()

def transform_reviews_to_dict(reviews):
    reviews_by_game = {}
    for game_id, review in reviews:
        if game_id not in reviews_by_game:
            reviews_by_game[game_id] = []
        reviews_by_game[game_id].append(review)
    return reviews_by_game

# 리뷰를 딕셔너리 형태로 변환
def get_all_reviews():
    positive_reviews = fetch_Positive_reviews()
    negative_reviews = fetch_Negative_reviews()

    positive_reviews_by_game = transform_reviews_to_dict(positive_reviews)
    negative_reviews_by_game = transform_reviews_to_dict(negative_reviews)

    return positive_reviews_by_game, negative_reviews_by_game

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
        category_id = get_category_id(category)
        if category_id is not None:
            cursor.execute(
                "INSERT INTO word (similar_word, category_id) VALUES (%s, %s)",
                (similar_word, category_id)
            )
    conn.commit()
    conn.close()

# # 요약된 리뷰를 데이터베이스에 저장하는 함수
def store_summaries(gameID, category_id, summary, polarity):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 중복 확인
    cursor.execute(
        "SELECT COUNT(*) FROM summary_review WHERE game_id = %s AND category_id = %s AND Polarity = %s",
        (gameID, category_id, polarity)
    )
    count = cursor.fetchone()[0]

    if count == 0:
        # 요약을 삽입
        try:
            query = "INSERT INTO summary_review (summary_review, game_id, category_id, Polarity) VALUES (%s, %s, %s, %s)"
            params = (summary, gameID, category_id, polarity)
            print(f"Executing query: {query}")
            print(f"With parameters: {params}")
            cursor.execute(query, params)
        except Exception as e:
            print(f"Error storing summary for gameID {gameID}, category_id {category_id}: {e}")

    conn.commit()
    conn.close()


def store_summaries_for_all_games_positive(summaries_by_category):
    category_map = {
        'graphic': 1,
        'story': 2,
        'sound': 3,
        'creative': 4
    }

    for category, games in summaries_by_category.items():
        category_id = category_map.get(category)
        if category_id is None:
            print(f"Unknown category: {category}")
            continue

        for game_id, summary in games.items():
            # 긍정적 및 부정적 요약을 구분하여 저장
            polarity = 'positive'
            print(f"Storing summary for gameID {game_id}, category_id {category_id}: Polarity = {polarity}")
            store_summaries(game_id, category_id, summary, polarity)

def store_summaries_for_all_games_negative(summaries_by_category):
    category_map = {
        'graphic': 1,
        'story': 2,
        'sound': 3,
        'creative': 4
    }

    for category, games in summaries_by_category.items():
        category_id = category_map.get(category)
        if category_id is None:
            print(f"Unknown category: {category}")
            continue

        for game_id, summary in games.items():
            # 긍정적 및 부정적 요약을 구분하여 저장
            polarity = 'negative'
            print(f"Storing summary for gameID {game_id}, category_id {category_id}: Polarity = {polarity}")
            store_summaries(game_id, category_id, summary, polarity)
