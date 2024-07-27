import mysql.connector
import fasttext
import re
import nltk
from collections import defaultdict
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer


def load_FestText():
    loaded_model = fasttext.load_model("fasttext_review_model.bin")
    return loaded_model

# 유사한 단어 찾기(이미 있는 키워드가 포함된 단어 빼고 찾기)
def find_similar_keywords(model, text, top_n, extracted_keywords):

    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer

    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    lemma = lemmatizer.lemmatize(text, pos='n')
    words = word_tokenize(lemma)
    similar_words = []

    for word in words:
        if word in extracted_keywords:
            continue

        similar = model.get_nearest_neighbors(word) 
        for sim_word, score in similar:
            if score >= 0.7 and sim_word not in extracted_keywords:
                similar_words.append(sim_word)
                extracted_keywords.add(sim_word)
                if len(similar_words) >= top_n:
                    break
   
    return similar_words

# 카테고리를 지정하여 키워드를 리스트로 받고 반환하기
def  extract_similar_keywords_by_category(reviews, model, top_n):

    keywords_by_category = {}
    categories = ['graphic', 'sound', 'story', 'creativity']
    
    extracted_keywords = set()  # set으로 선언해서 중복을 방지함.
    all_reviews = " ".join(review['review'] for review in reviews)

    for category in categories:
        similar_words = find_similar_keywords(model, all_reviews, top_n, extracted_keywords)
        keywords_by_category[category] = similar_words

    return keywords_by_category

#여기서 키워드가 포함된 문장 추출하고 키워드별 코퍼스 반환(review에서)
#sound, graphic, creative, story
def find_sentence(text, word):
    nltk.download('punkt')
    word = word.lower()
    result_sentence = []

    # 문장을 마침표, 느낌표 같은 문장 구분기호를 기준으로 나눔
    sentences = sent_tokenize(text)
    
    for sentence in sentences:
        # 문장에 word가 있으면 result_sentence에 넣기
        if word in sentence.lower():
            result_sentence.append(sentence)
    
    result = ' '.join(result_sentence)
    return result

#키워드가 포함된 코퍼스들을 훈련된 모델로 요약하는 함수
#def summrize_by_Pegasus(keywords):     
