from summarize import find_similar_words,train_fasttext_model,load_pegasus_model
from collections import defaultdict
from summarize import summarize_reviews
from preDataBase import store_summaries
model = train_fasttext_model()
tokenizer, pegasus_model = load_pegasus_model()

mydb=get_db_connection()
cursor=mydb.cursor()
data = fetch_reviews(cursor)



#요약한걸 데이터베이스에 올린다.               
store_summaries(cursor, reviews_by_game_and_category)

