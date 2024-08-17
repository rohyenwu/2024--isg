import torch
import fasttext
import nltk
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def load_FestText():
    loaded_model = fasttext.load_model("/Users/iusong/2024--isg-1/fasttext_review_model.bin")
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
    return model, tokenizer, device

def find_similar_keywords(model, keyword, top_n):
    similar_words = []

    # 유사 단어와 유사도 쌍을 리스트로 가져옵니다.
    similar = model.get_nearest_neighbors(keyword, k=top_n + 1000)  # 추가로 10개 더 가져와서 필터링합니다.

    # 유사도와 단어 쌍을 리스트로 저장합니다.
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
        'creative': ['creative']
    }

    similar_keywords_by_category = {}

    for category, exclude_words in categories.items():
        similar_words = find_similar_keywords(model, category, top_n)
        filtered_words = [(word, score) for word, score in similar_words if not contains_substring(exclude_words, word)]

        # 유사도 순으로 정렬합니다.
        sorted_words = sorted(filtered_words, key=lambda x: x[1], reverse=True)

        # 상위 top_n개의 단어를 선택합니다.
        top_words = [word for word, _ in sorted_words[:top_n]]

        similar_keywords_by_category[category] = top_words

    return similar_keywords_by_category

def filter_top_n_games(reviews_by_game, n=10):
    # game_ids는 reviews_by_game의 키들로부터 가져옵니다
    game_ids = list(reviews_by_game.keys())[:n]
    # 선택된 게임 ID에 해당하는 리뷰만 필터링합니다
    filtered_reviews = {game_id: reviews_by_game[game_id] for game_id in game_ids}
    return filtered_reviews


def find_sentence(text, word):
    # 단어를 소문자로 변환하여 대소문자 구분 없이 검색
    word = word.lower()

    # 문장을 마침표를 기준으로 나눔
    sentences = text.split('.')

    result_sentence = []

    for sentence in sentences:
        # 각 문장의 양쪽 공백 제거
        sentence = sentence.strip()
        if sentence and word in sentence.lower():
            result_sentence.append(sentence)

    # 문장 리스트를 다시 하나의 문자열로 합침
    result = '. '.join(result_sentence)
    return result


def extract_sentences_by_keywords(reviews_by_game, keywords_by_category):
    sentences_by_category = {}

    # 카테고리별 문장을 저장할 딕셔너리 초기화
    categories = set(category for category, _ in keywords_by_category)
    for category in categories:
        sentences_by_category[category] = {}

    # 카테고리와 키워드에 대해 문장 추출
    for category, keyword in keywords_by_category:
        if category not in sentences_by_category:
            sentences_by_category[category] = {}

        # 각 게임의 리뷰에서 문장 추출
        for game_id, reviews in reviews_by_game.items():
            for review in reviews:
                if isinstance(review, str):
                    sentences = find_sentence(review, keyword)
                    if sentences:
                        if game_id not in sentences_by_category[category]:
                            sentences_by_category[category][game_id] = []
                        sentences_by_category[category][game_id].append(sentences)
                else:
                    print(f"Expected string but got {type(review)}.")

    return sentences_by_category


def summarize_text(text, model, tokenizer, device):
    inputs = tokenizer(text, return_tensors="pt", truncation=False, padding=True)

    # 모델과 입력을 MPS 장치로 이동
    model = model.to(device)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # attention_mask 추가
    inputs["attention_mask"] = inputs["attention_mask"].to(device)

    # 요약 생성
    summary_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        num_beams=4,
        min_length=30,
        max_length=200,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def convert_list_to_dict(data_list):
    result = {}
    for item in data_list:
        # 여기서 item이 적절한 형태의 딕셔너리라고 가정
        category = item['category']
        game_id = item['game_id']
        if category not in result:
            result[category] = {}
        if game_id not in result[category]:
            result[category][game_id] = []
        result[category][game_id].append(item['sentence'])
    return result

# #키워드가 포함된 코퍼스들을 훈련된 모델로 요약하는 함수
def summarize_by_Pegasus(sentences_by_category):
    model, tokenizer, device = load_Pegasus()
    summaries_by_category = {}

    print("Type of sentences_by_category:", type(sentences_by_category))

    if isinstance(sentences_by_category, list):
        print("Converting list to dictionary...")
        sentences_by_category = convert_list_to_dict(sentences_by_category)

    if not isinstance(sentences_by_category, dict):
        raise ValueError("Expected a dictionary for sentences_by_category.")

    for category, games in sentences_by_category.items():
        summaries_by_category[category] = {}

        for game_id, sentences in games.items():
            combined_text = ' '.join(sentences)
            if len(combined_text) > tokenizer.model_max_length:
                print(f"Text for game {game_id} in category {category} is too long. Truncating...")
                combined_text = combined_text[:tokenizer.model_max_length]  # Truncate text

            summary = summarize_text(combined_text, model, tokenizer, device)
            summaries_by_category[category][game_id] = summary

    print("Type of summaries_by_category:", type(summaries_by_category))
    return summaries_by_category

#점수 산출
def calculate_score(positiveNum,negativeNum):
    allNum=positiveNum+negativeNum
    score=positiveNum/allNum
    return score
    
