import mysql.connector
import fasttext
from collections import defaultdict
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# 데이터베이스 연결
conn = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

cursor = conn.cursor()

# 데이터베이스에서 카테고리 ID를 가져오는 함수
def get_category_id(category_type):
    cursor.execute("SELECT category_id FROM category WHERE category_type = %s", (category_type,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"Category '{category_type}' not found.")
        return None

# 데이터베이스에서 리뷰 데이터를 가져오기
cursor.execute("SELECT game_id, review FROM game_reviews")
data = cursor.fetchall()

# FastText 모델 훈련시키기
model = fasttext.train_unsupervised('reviews.txt', model='skipgram', minCount=1)
model.save_model('reviews_model.bin')

# 단어 임베딩 결과 확인하기
def find_similar_words(word, top_n=10):
    try:
        similar_words = model.get_nearest_neighbors(word, k=top_n)
        return similar_words
    except Exception as e:
        print(f"Error: {e}")
        return []

# 예시 단어
categories = ['graphic', 'sound', 'story', 'convenience', 'creativity']
keyWords = []

for category in categories:
    similar_words = find_similar_words(category, top_n=10)
    for score, similar_word in similar_words:
        if score > 0.7:  # score 임계값을 설정하여 신뢰할 수 있는 유사 단어만 포함
            keyWords.append((category, similar_word))

# 추출된 키워드를 데이터베이스에 저장하기
for category, similar_word in keyWords:
    category_id = get_category_id(category)
    if category_id is not None:
        cursor.execute(
            "INSERT INTO word (similar_word, category_id) VALUES (%s, %s)",
            (similar_word, category_id)
        )

# 리뷰에서 키워드가 포함된 리뷰를 게임별로, 그리고 카테고리별로 그룹화하기
reviews_by_game_and_category = defaultdict(lambda: defaultdict(list))

for category, similar_word in keyWords:
    category_id = get_category_id(category)
    if category_id is not None:
        for game_id, review in data:
            if similar_word.lower() in review.lower():  # 대소문자 무시
                reviews_by_game_and_category[game_id][category_id].append(review)


# Pegasus 모델 로드
model_name = 'google/pegasus-xsum'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)

# 게임별로, 그리고 카테고리별로 리뷰 요약하기
def summarize_reviews(reviews):
    # 리뷰 데이터가 리스트인지 확인
    if not isinstance(reviews, list):
        raise TypeError("Expected 'reviews' to be a list of dictionaries.")
    
    # 각 리뷰에서 'review_text' 필드를 추출하여 텍스트를 합칩니다.
    combined_reviews = " ".join([review['review_text'] for review in reviews if isinstance(review, dict) and 'review_text' in review])
    
    # 텍스트를 토큰화합니다. max_length를 적절히 설정합니다.
    inputs = tokenizer(combined_reviews, max_length=1024, return_tensors='pt', truncation=True, padding='longest')
    
    # 토큰화된 입력의 길이 확인
    input_ids = inputs.input_ids
    print(f"Input IDs length: {input_ids.size()}")  # 디버깅을 위한 출력
    
    # 텍스트 요약 생성
    summary_ids = pegasus_model.generate(input_ids, num_beams=4, max_length=200, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary



# 요약된 리뷰를 summury_review 테이블에 저장하기
for game_id, categories in reviews_by_game_and_category.items():
    for category_id, reviews in categories.items():
        summary = summarize_reviews(reviews)
        cursor.execute(
            "INSERT INTO summury_review (summury_review, game_id, category_id) VALUES (%s, %s, %s)",
            (summary, game_id, category_id)
        )

# 변경 사항 저장 및 연결 종료
conn.commit()
conn.close()

# 추출된 카테고리 및 유사 단어 출력
for category, similar_word in keyWords:
    print(f"Category: {category}, Similar Word: {similar_word}")


