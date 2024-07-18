import pandas as pd
import fasttext

# CSV 파일 읽기
df = pd.read_csv("/Users/iusong/Downloads/positive.csv")  #
# 리뷰 텍스트 추출
reviews = df['Review Text'].tolist()

# 리뷰 텍스트를 텍스트 파일로 저장
with open("reviews.txt", "w", encoding="utf-8") as f:
    for review in reviews:
        f.write(f"{review}\n")

# 모델 훈련
model = fasttext.train_unsupervised("reviews.txt", model='skipgram', epoch=5, lr=0.05, dim=100)

# 모델 저장
model_save_path = "fasttext_review_model.bin"
model.save_model(model_save_path)
print(f"Model saved to {model_save_path}")

# 모델 로드
loaded_model = fasttext.load_model(model_save_path)

word = "sound"  # 유사 단어를 찾고 싶은 단어로 변경
similar_words = loaded_model.get_nearest_neighbors(word, k=100)

# 유사 단어 출력
print(f"Words similar to '{word}':")
for score, similar_word in similar_words:
    print(f"{similar_word} (similarity: {score})")