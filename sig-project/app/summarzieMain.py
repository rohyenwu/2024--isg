from summarize import find_similar_words,train_fasttext_model,load_pegasus_model
from database import get_category_id, fetch_reviews, store_keywords,get_db_connection,store_summaries
from collections import defaultdict
from summarize import summarize_reviews
model = train_fasttext_model()
tokenizer, pegasus_model = load_pegasus_model()

mydb=get_db_connection
cursor=mydb.cursor()
data = fetch_reviews(cursor)

# 키워드를 찾아서 데이터베이스에 올린다.
keywords_by_category = extract_similar_keywords_by_category(data, model, top_n=10)

#요약한걸 데이터베이스에 올린다.               
store_summaries(cursor, reviews_by_game_and_category)

