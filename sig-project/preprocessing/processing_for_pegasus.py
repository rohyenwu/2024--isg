import pandas as pd
import pickle
from sklearn.model_selection import train_test_split

# CSV 파일 경로
positive_csv_path = '/Users/iusong/Downloads/Positive2.csv'
negative_csv_path = '/Users/iusong/Downloads/Negative2.csv'

# CSV 파일 로드
positive_df = pd.read_csv(positive_csv_path)
negative_df = pd.read_csv(negative_csv_path)

# 'Review Text' 컬럼만 추출
positive_reviews = positive_df['game_reviews_positive'].tolist()
negative_reviews = negative_df['Review Text'].tolist()

# 문자열만 필터링
positive_reviews = [review for review in positive_reviews if isinstance(review, str)]
negative_reviews = [review for review in negative_reviews if isinstance(review, str)]

# 데이터셋 크기를 10분의 1로 줄임
reduced_positive_reviews = positive_reviews[:len(positive_reviews)//10]
reduced_negative_reviews = negative_reviews[:len(negative_reviews)//10]

# 데이터 합치기
all_reviews = reduced_positive_reviews + reduced_negative_reviews

# 데이터를 훈련 및 검증 세트로 분리
train_texts, val_texts = train_test_split(all_reviews, test_size=0.2, random_state=42)

# 전처리된 데이터 저장
preprocessed_data = {
    'train_texts': train_texts,
    'val_texts': val_texts
}

preprocessed_data_path = "/Users/iusong/2024--isg-1/preprocessed_data.pkl"
with open(preprocessed_data_path, 'wb') as f:
    pickle.dump(preprocessed_data, f)

print("전처리된 데이터가 저장되었습니다.")
