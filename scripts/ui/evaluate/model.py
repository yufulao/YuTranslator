# ui/evaluate/model.py
import evaluate
import nltk
from bert_score import score  # 只导入 score 函数
import jieba

# 下载 METEOR 所需的词典（只需要一次）
nltk.download("wordnet")
nltk.download("punkt")

# 加载评估指标
bleu = evaluate.load("bleu")
chrf = evaluate.load("chrf")
meteor = evaluate.load("meteor")

class EvaluateModel:
    def __init__(self):
        # 这里不需要使用 BERTScore 类，直接使用 score 函数
        pass

    def evaluate(self, algorithm, predictions, references, lang=None):
        # 根据选择的评估算法进行评估
        if algorithm == "BLEU":
            predictions = [" ".join(jieba.cut(s)) for s in predictions]
            references = [[" ".join(jieba.cut(s)) for s in ref_list] for ref_list in references]
            # print(predictions)
            # print(references)
            result = bleu.compute(predictions=predictions, references=references)
            return f"BLEU: {result['bleu']:.4f}"
        
        elif algorithm == "CHRF":
            result = chrf.compute(predictions=predictions, references=references)
            return f"CHRF: {result['score']:.4f}"
        
        elif algorithm == "METEOR":
            result = meteor.compute(predictions=predictions, references=references)
            return f"METEOR: {result['meteor']:.4f}"
        
        elif algorithm == "BERTScore F1":
            P = predictions
            R = references[0]  # references 是二维列表，取第一个参考翻译集合
            P, R, F1 = score(P, R, lang=lang, verbose=True)
            return f"BERTScore F1: {F1[0]:.4f}"
        
        return "未知算法"
