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


# #각 카테고리별로 키워드 찾는 함수
# #여기서 카테고리별로 키워드를 찾는데 ex)sound찾으면 sound포함된 단어빼고, 다음으로 유사도 높은단어 이런식으로 10개
# def find_Key_words(model, word, top_n=10):


# #여기서 키워드가 포함된 문장 추출하고 키워드별 코퍼스 반환(review에서)
# #sound, graphic, creative, story
# def find_sentence(word):

# #키워드가 포함된 코퍼스들을 훈련된 모델로 요약하는 함수
# def summrize_by_Pegasus(keywords):

