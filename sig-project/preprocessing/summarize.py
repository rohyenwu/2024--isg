import torch
import fasttext
import nltk
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

def find_similar_keywords(model, keyword, top_n):
    similar_words = []
    similar = model.get_nearest_neighbors(keyword, k=top_n + 1000)  # 추가로 1000개 더 가져와서 필터링

    similar_words = [(word, score) for score, word in similar]  # (단어, 유사도) 순으로 정렬

    return similar_words

def contains_substring(keywords, candidate):
    return any(keyword.lower() in candidate.lower() for keyword in keywords)

# 카테고리별로 유사한 키워드를 추출하는 함수
def extract_similar_keywords_by_category(model, top_n):
    categories = {
        'graphic': ['graphic'],
        'sound': ['sound'],
        'story': ['story'],
        'creativity': ['creativity']
    }

    similar_keywords_by_category = {}

    for category, exclude_words in categories.items():
        similar_words = find_similar_keywords(model, category, top_n)
        filtered_words = [(word, score) for word, score in similar_words if not contains_substring(exclude_words, word)]
        sorted_words = sorted(filtered_words, key=lambda x: x[1], reverse=True)
        top_words = [word for word, _ in sorted_words[:top_n]]

        similar_keywords_by_category[category] = top_words

    return similar_keywords_by_category



def find_sentence(text, word):
    nltk.download('punkt')
    word = word.lower()
    result_sentence = []

    # 문장을 마침표, 느낌표 같은 문장 구분기호를 기준으로 나눔
    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:
        # 문장에 word가 있으면 result_sentence에 넣기
        if word in sentence.lower():
            result_sentence.append(sentence)

    result = ' '.join(result_sentence)
    return result

# #키워드가 포함된 코퍼스들을 훈련된 모델로 요약하는 함수
# def summrize_by_Pegasus(keywords):
