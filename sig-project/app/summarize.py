import mysql.connector
import fasttext
from collections import defaultdict
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

global tokenizer, pegasus_model




# FastText 모델 훈련시키기
def train_fasttext_model(file_path='reviews.txt'):
    model = fasttext.train_unsupervised(file_path, model='skipgram', minCount=1)
    model.save_model('reviews_model.bin')
    return model

# 단어 임베딩 결과 확인하기
def find_similar_words(model, word, top_n=10):
    try:
        similar_words = model.get_nearest_neighbors(word, k=top_n)
        return similar_words
    except Exception as e:
        print(f"Error: {e}")
        return []

# Pegasus 모델 로드
def load_pegasus_model(model_name='google/pegasus-xsum'):
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

# 리뷰 요약하기
#ex) 추출한 키워드들 그거 가지고 이제 문장을 뽑아서 그 문장들을 다 합쳐서 요약한다. 
def summarize_reviews(reviews):
    if not isinstance(reviews, list):
        raise TypeError("Expected 'reviews' to be a list of strings.")
    
    combined_reviews = " ".join(reviews)
    
    max_input_length = 1024
    if len(tokenizer(combined_reviews, return_tensors='pt', truncation=False)['input_ids'][0]) > max_input_length:
        combined_reviews = tokenizer.decode(tokenizer(combined_reviews, max_length=max_input_length, return_tensors='pt', truncation=True)['input_ids'][0])
    
    inputs = tokenizer(combined_reviews, max_length=max_input_length, return_tensors='pt', truncation=True, padding='longest')
    
    input_ids = inputs.input_ids
    print(f"Input IDs length: {input_ids.size()}")
    
    try:
        summary_ids = pegasus_model.generate(input_ids, num_beams=4, max_length=200, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error generating summary: {e}")
        summary = ""
    return summary