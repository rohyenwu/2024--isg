import mysql.connector
import fasttext
from collections import defaultdict
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def load_FestText():
    loaded_model = fasttext.load_model("fasttext_review_model.bin")
    return loaded_model

#모델이랑 토크나이저 같이 반환한다.
def load_Pegasus():
    #모델 로드할 때 mps장치로 올리기
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    model_save_path = "/Users/iusong/2024--isg-1/trained_pegasus_model"
    #모델이랑 토크나이저 로드
    model = PegasusForConditionalGeneration.from_pretrained(model_save_path).to(device)
    tokenizer = PegasusTokenizer.from_pretrained(model_save_path)
    return model, tokenizer

# FastText 모델을 사용하여 유사한 단어를 찾는 함수
def find_similar_keywords(model, keyword, top_n):
    similar_words = []
    extracted_words = [keyword] 

    # 유사 단어 추출
    similar = model.get_nearest_neighbors(keyword)
    for sim_word, _ in similar:
        if not contains_substring(extracted_words, sim_word):
            similar_words.append(sim_word)
            extracted_words.append(sim_word)
            if len(similar_words) >= top_n:
                break

    return similar_words

# 카테고리별로 유사한 키워드를 추출하는 함수
def extract_similar_keywords_by_category(model, top_n):
    categories = ['graphic', 'sound', 'story', 'convenience', 'creativity']
    similar_keywords_by_category = {}

    for category in categories:
        similar_words = find_similar_keywords(model, category, top_n)
        similar_keywords_by_category[category] = similar_words

    return similar_keywords_by_category

# 특정 문자열이 다른 문자열의 부분 문자열인지 확인하는 함수
def contains_substring(keywords, candidate):
    return any(keyword in candidate for keyword in keywords)


# #여기서 키워드가 포함된 문장 추출하고 키워드별 코퍼스 반환(review에서)
# #sound, graphic, creative, story
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

# #키워드가 포함된 코퍼스들을 훈련된 모델로 요약하는 함수
# def summrize_by_Pegasus(keywords):

