import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments
import torch
from transformers import DataCollatorForSeq2Seq


# MPS 장치 사용 설정
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

# CSV 파일 읽기
df = pd.read_csv("/Users/iusong/Downloads/positive.csv")  # 파일 경로를 실제 파일 경로로 변경

# 텍스트 데이터 필터링 (문자열 형식만 남기기)
df = df[df['Review Text'].apply(lambda x: isinstance(x, str))]

# 리뷰 텍스트 추출
texts = df['Review Text'].tolist()

# 데이터 분할 (훈련 및 검증 데이터셋)
train_texts, val_texts = train_test_split(texts, test_size=0.1, random_state=42)

# 모델 및 토크나이저 불러오기
model_name = "google/pegasus-cnn_dailymail"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

# 데이터셋 클래스 정의
class TextDataset(torch.utils.data.Dataset):
    def __init__(self, tokenizer, texts, block_size=1024):
        self.examples = []
        for text in texts:
            tokenized_input = tokenizer(text, max_length=block_size, truncation=True, padding="max_length", return_tensors="pt")
            input_ids = tokenized_input["input_ids"][0].to(device)
            attention_mask = tokenized_input["attention_mask"][0].to(device)
            target_ids = input_ids.clone()
            target_ids[target_ids == tokenizer.pad_token_id] = -100  # 패딩 토큰에 대한 마스크 설정
            self.examples.append({
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "labels": target_ids
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        return self.examples[item]

# 데이터셋 준비
train_dataset = TextDataset(tokenizer, train_texts)
val_dataset = TextDataset(tokenizer, val_texts)

# 훈련 인자 설정
training_args = TrainingArguments(
    output_dir='./results',          
    num_train_epochs=3,              
    per_device_train_batch_size=2,   
    per_device_eval_batch_size=2,    
    save_steps=500,                 
    save_total_limit=2,             
    eval_strategy='epoch',          
    logging_dir='./logs',            
)

# 트레이너 정의
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# 모델 훈련
trainer.train()

# 모델 저장
model_save_path = "./trained_pegasus_model"
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)

print(f"Model saved to {model_save_path}")

# 모델 및 토크나이저 로드
model = PegasusForConditionalGeneration.from_pretrained(model_save_path).to(device)
tokenizer = PegasusTokenizer.from_pretrained(model_save_path)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
model.to(device)


# 요약 생성 함수
def summarize(text, model, tokenizer, max_length=60, num_beams=5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="longest", max_length=512).to(device)
    summary_ids = model.generate(inputs['input_ids'], num_beams=num_beams, max_length=max_length, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# 테스트용 텍스트
test_text = "Your test review text goes here."

# 요약 생성
summary = summarize(test_text, model, tokenizer)
print("Summary: ", summary)
