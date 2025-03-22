import langdetect
import torch
import config
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class M2M100Translator:
    def __init__(self, model_path):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # 加载模型和tokenizer，并将其移动到 GPU
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_path)
        self.model = M2M100ForConditionalGeneration.from_pretrained(model_path).to(device)
        self.device = device  # 记住设备，后续操作需要用到

    def generate_text(self, input_text, target_language, *arg):
        # 自动检测源语言
        src_lang = langdetect.detect(input_text)
        if src_lang == "zh-cn" or src_lang == "zh-tw":
            src_lang = "zh"
            
        # 编码输入文本
        print(input_text)
        encoded = self.tokenizer(input_text, return_tensors="pt").to(self.device)
        generated_tokens = self.model.generate(**encoded, forced_bos_token_id=self.tokenizer.get_lang_id(target_language))

        # 解码输出并返回
        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        # return self.tokenizer.decode(generated_tokens[0], skip_special_tokens=True)