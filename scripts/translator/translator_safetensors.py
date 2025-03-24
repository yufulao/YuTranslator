import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from gptqmodel import GPTQModel

class SafetensorsTranslator:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"  # 自动检测 GPU
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        
        if "GPTQ" in model_path or "gptq" in model_path:
            self.model = GPTQModel.load(
                model_path,
                # device_map="auto",  # 自动选择设备
                # use_safetensors=True,  # 使用 safetensors
            ).to(self.device)
            return
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
        ).to(self.device)

    def generate_text(self, input_text, target_language, *arg):
        prompt = f"翻译以下文字为 {target_language}:\n\n{input_text}\n\n翻译结果:"
        inputs = self.tokenizer(prompt, return_tensors="pt")  
        inputs = {k: v.to(self.device) for k, v in inputs.items()}  # 确保输入张量在 GPU
        outputs = self.model.generate(
            **inputs,
            max_length=256,  # 限制生成的最大长度
            temperature=0.1,  # 降低温度，减少随机性
            do_sample=True,  # 启用采样
            repetition_penalty=1.2,  # 减少重复惩罚，避免模型过于拘谨
            top_p=0.9,  # 控制生成的多样性，减少不合理输出
            top_k=30,  # 限制采样范围，避免无关内容
        )
        
        output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        result = self._process_output(output)
        
        print(f"==================================\nprompt: \n{prompt}\n==================================")
        print(f"==================================\noutput: \n{output}\n==================================")
        print(f"==================================\nresult: \n{result}\n==================================")
        
        return result
    
    #处理输出
    def _process_output(self, output:str):
        if "翻译结果:" in output:
            # 找到 "翻译结果:" 的位置，并截取后面的内容
            result = output.split("翻译结果:")[1].strip()
        else:
            # 如果没有找到 "翻译结果:"，返回完整内容
            result = output.strip()
        return result