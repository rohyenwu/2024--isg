import pandas as pd
import fasttext

# CSV 파일 읽기
df1 = pd.read_csv("/Users/iusong/Downloads/negative.csv")
df2 = pd.read_csv("/Users/iusong/Downloads/positive.csv")
reviews1 = df1['Review Text'].tolist()
reviews2 = df2['Review Text'].tolist()
# 리뷰 텍스트를 텍스트 파일로 저장

with open("positive.txt", "w", encoding="utf-8") as f:
    for review in reviews1:
        f.write(f"{review}\n")

with open("negative.txt", "w", encoding="utf-8") as f:
    for review in reviews2:
        f.write(f"{review}\n")


# 모델 훈련
model = fasttext.train_unsupervised("positive.txt", model='skipgram', epoch=5, lr=0.05, dim=100)
model = fasttext.train_unsupervised("negative.txt", model='skipgram', epoch=5, lr=0.05, dim=100)

# 모델 저장
model_save_path = "fasttext_review_model.bin"
model.save_model(model_save_path)
print(f"Model saved to {model_save_path}")

loaded_model = fasttext.load_model(model_save_path)
word = "sound"  # 유사 단어를 찾고 싶은 단어로 변경
similar_words = loaded_model.get_nearest_neighbors(word, k=100)

# 유사 단어 출력
print(f"Words similar to '{word}':")
for score, similar_word in similar_words:
    print(f"{similar_word} (similarity: {score})")