import sys
import os
import config

path_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(path_root)
sys.path.insert(0, config.LIB_DIR)


import evaluate
import nltk
from transformers import pipeline

# 下载 METEOR 所需的词典（只需要一次）
nltk.download("wordnet")
nltk.download("punkt")

# 加载评估指标
bleu = evaluate.load("bleu")
chrf = evaluate.load("chrf")
meteor = evaluate.load("meteor")

# 原文（源语言）、预测翻译、参考翻译（目标语言）
sources = ["I went to the supermarket today."]
predictions = ["我今天去超市了。"]
references = [["今天我去超市了。"]]  # 多个参考翻译需用二维列表

# ========== 1. 常规评估 ==========
print("🚀 普通评估（需要参考翻译）:")
bleu_result = bleu.compute(predictions=predictions, references=references)
chrf_result = chrf.compute(predictions=predictions, references=references)
meteor_result = meteor.compute(predictions=predictions, references=references)

print(f"BLEU: {bleu_result['bleu']:.4f}")
print(f"CHRF: {chrf_result['score']:.4f}")
print(f"METEOR: {meteor_result['meteor']:.4f}")

from bert_score import score

P = ["我今天去超市了。"]
R = ["今天我去超市了。"]
P, R, F1 = score(P, R, lang="zh", verbose=True)
print(f"BERTScore F1: {F1[0]:.4f}")


# # ========== 2. 回译评估（Round-trip） ==========
# # 回译模型（英文→中文）
# back_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-zh")

# back_translations = []
# for text in predictions:
#     result = back_translator(text, max_length=100)
#     back_translations.append(result[0]["translation_text"])

# print("\n🔁 回译 BLEU 评估:")
# print("回译结果:", back_translations)

# # 回译 BLEU（对比回译结果和原中文）
# bleu_back = bleu.compute(predictions=back_translations, references=[[s] for s in sources])
# print(f"Round-trip BLEU: {bleu_back['bleu']:.4f}")
