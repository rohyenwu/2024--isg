from summarize import find_similar_words,train_fasttext_model,load_pegasus_model
from database import get_category_id, fetch_reviews, store_keywords,get_db_connection,store_summaries
from collections import defaultdict
from summarize import summarize_reviews
model = train_fasttext_model()
# Pegasus 모델 로드
tokenizer, pegasus_model = load_pegasus_model()
mydb=get_db_connection
cursor=mydb.cursor()
data = fetch_reviews(cursor)
# 키워드 데이터베이스에 저장
# 예시 단어와 유사 단어 추출
categories = ['graphic', 'sound', 'story', 'convenience', 'creativity']
keyWords = []
for category in categories:
    similar_words = find_similar_words(model, category, top_n=10)
    for score, similar_word in similar_words:
        if score > 0.5:
            keyWords.append((category, similar_word))
store_keywords(cursor, keyWords)



# 키워드가 포함된 리뷰를 게임별로, 그리고 카테고리별로 그룹화 
# 각 카테고리별 키워드들이 포함된 문장들을 뽑는다.
reviews_by_game_and_category = defaultdict(lambda: defaultdict(list))
for category, similar_word in keyWords:
    category_id = get_category_id(cursor, category)
    if category_id is not None:
        for game_id, review in data:
            if similar_word.lower() in review.lower():
                reviews_by_game_and_category[game_id][category_id].append(review)

summarize_reviews()
#요약한걸 데이터베이스에 올린다.               
store_summaries(cursor, reviews_by_game_and_category)

