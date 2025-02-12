from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

# 选择模型
model_name = "../models/DeepSeek-R1-8B"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # 自动分配 GPU/CPU
    load_in_4bit=True,  # 4-bit 量化
    torch_dtype=torch.float16  # 适配 FP16
)


def translate(text, src_lang="English", tgt_lang="Chinese"):
    # 构造翻译指令
    prompt = f"Translate the following {src_lang} text to {tgt_lang}: {text}"

    # 编码输入文本
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    # 生成翻译结果
    output = model.generate(**inputs, max_new_tokens=100)

    # 解码输出
    translated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return translated_text

# 测试翻译
text = "Hello, how are you today?"
translated_text = translate(text, "Chinese")  # 翻译成中文
print(translated_text)
