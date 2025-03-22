import llama_cpp
import torch

class GGUFTranslator:
    def __init__(self, model_path):
        self.llm = llama_cpp.Llama(
            model_path=model_path,
            n_gpu_layers=100, 
            verbose=False, #日志
            use_cuda=True,
            gpu_device=0,
            # n_batch=512,  # 增大批处理大小，加速推理
            # use_mlock=True,  # 锁定模型到内存，避免交换到磁盘
        )

        print(f"CUDA 是否可用: {torch.cuda.is_available()}")
        print(f"GPU 数量: {torch.cuda.device_count()}")
        print(f"当前 GPU: {torch.cuda.current_device()}")
        print(f"GPU 名称: {torch.cuda.get_device_name(0)}")
        print(f"模型加载的model: {self.llm.model}")
        print(f"GPU 内存总量: {torch.cuda.get_device_properties(0).total_memory / 1024 ** 2} MB")
        print(f"GPU 内存已用: {torch.cuda.memory_allocated(0) / 1024 ** 2} MB")
        print(f"GPU 内存剩余: {torch.cuda.memory_reserved(0) / 1024 ** 2} MB")

    def generate_text(self, input_text, target_language, *arg):
        print(arg)
        temperature, max_tokens, top_p = arg
        prompt = f"翻译以下文字为 {target_language}:\n\n{input_text}\n\n翻译结果:"
        
        result = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=["\n\n"],
            temperature=temperature,
            top_p=top_p,
        )

        print(prompt)
        print(result)
        return result["choices"][0]["text"].strip()