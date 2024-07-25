import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments
import pickle
# MPS 디바이스 설정
# device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
# MPS 디바이스 설정
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")
# 전처리된 데이터 로드
preprocessed_data_path = "your csv path"
with open(preprocessed_data_path, 'rb') as f:
    preprocessed_data = pickle.load(f)

train_texts = preprocessed_data['train_texts']
val_texts = preprocessed_data['val_texts']
# 모델 및 토크나이저 불러오기
model_save_path = "/Users/iusong/2024--isg-1/trained_pegasus_model"
tokenizer = PegasusTokenizer.from_pretrained(model_save_path)
model = PegasusForConditionalGeneration.from_pretrained(model_save_path).to(device)
# 데이터셋 클래스 정의
class TextDataset(torch.utils.data.Dataset):
    def __init__(self, tokenizer, texts, block_size=512):
        self.examples = []
        for text in texts:
            # Tokenization
            tokenized_input = tokenizer(text, max_length=block_size, truncation=True, padding="max_length", return_tensors="pt")
            input_ids = tokenized_input["input_ids"].squeeze(0).to(device)
            attention_mask = tokenized_input["attention_mask"].squeeze(0).to(device)

            # Prepare labels
            target_ids = input_ids.clone()
            target_ids[target_ids == tokenizer.pad_token_id] = -100  # Mask padding tokens for loss calculation

            self.examples.append({
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "labels": target_ids
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        # Retrieve the item
        example = self.examples[item]
        return {
            'input_ids': example['input_ids'],
            'attention_mask': example['attention_mask'],
            'labels': example['labels']
        }

# 데이터셋 준비
train_dataset = TextDataset(tokenizer, train_texts)
val_dataset = TextDataset(tokenizer, val_texts)
# TrainingArguments 설정
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=1,
    weight_decay=0.01,
    push_to_hub=False,
    use_mps_device=True,  # MPS 디바이스 사용
)

# Trainer 초기화
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)
# 모델 훈련
trainer.train()
# 모델 저장
model_save_path = "/Users/iusong/2024--isg-1/trained_pegasus_model2"
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)

print(f"Model saved to {model_save_path}")