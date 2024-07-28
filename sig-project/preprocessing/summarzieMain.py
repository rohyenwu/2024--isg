from summarize import extract_similar_keywords_by_category,train_fasttext_model,load_FestText,load_pegasus_model
from collections import defaultdict
from summarize import summarize_reviews
from preDataBase import store_summaries,get_db_connection, fetch_reviews,convert_keywords,store_keywords
model = train_fasttext_model()
tokenizer, pegasus_model = load_pegasus_model()
fasttext_model = load_FestText()

mydb=get_db_connection()
cursor=mydb.cursor()
data = fetch_reviews(cursor)

# 카테고리별 유사 키워드 추출
keywords = extract_similar_keywords_by_category(model, top_n=10)

keywords_by_category = convert_keywords(keywords)
store_keywords(keywords_by_category)


#요약한걸 데이터베이스에 올린다.               
store_summaries(cursor, )
