"""
下载预训练 BERT 中文模型到 bert-local/ 目录
运行: python download_bert.py
"""
from transformers import BertTokenizer, BertForSequenceClassification
import os

MODEL_NAME = "bert-base-chinese"
SAVE_DIR = "./bert-local"

os.makedirs(SAVE_DIR, exist_ok=True)

print(f"正在下载 {MODEL_NAME} ...")
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

tokenizer.save_pretrained(SAVE_DIR)
model.save_pretrained(SAVE_DIR)

print(f"✅ 模型已保存到 {SAVE_DIR}/")
