from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class BinTranslator:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"  # 选择 GPU 或 CPU
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(self.device)

    def generate_text(self, input_text, target_language, *arg):
        prompt = f"Translate the following text into {target_language}, just say the result:\n{input_text}"
        if not prompt.strip():
            return "请输入文本"
        
        # # 自动检测语言
        # detected_lang = langdetect.detect(prompt)
        # src_lang = config.LANG_MAP.get(detected_lang, "eng_Latn")  # 默认英文
        # print(detected_lang)
        # print(src_lang)
        # print(tgt_lang)
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        print(self.tokenizer.convert_tokens_to_ids(target_language))

        # 手动指定目标语言
        output_ids = self.model.generate(
            **inputs,
            forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(target_language)
        )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)