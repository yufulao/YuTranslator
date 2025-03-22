import torch
import config
from transformers import AutoTokenizer, AutoModelForCausalLM

class SafetensorsTranslator:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"  # 自动检测 GPU
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)
        #self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(self.device)

    def generate_text(self, input_text, target_language, *arg):
        prompt = f"Translate the following text into {target_language}, just say the result:\n{input_text}"
        inputs = self.tokenizer(prompt, return_tensors="pt")  
        inputs = {k: v.to(self.device) for k, v in inputs.items()}  # 确保输入张量在 GPU
        outputs = self.model.generate(**inputs, max_length=512, temperature=0.7, do_sample=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)