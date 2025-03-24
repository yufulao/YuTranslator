import os
import config
from peft import PeftModel, PeftConfig
from translator.translator_gguf import GGUFTranslator
from translator.translator_bin import BinTranslator
from translator.translator_safetensors import SafetensorsTranslator
from translator.translator_M2M100 import M2M100Translator

class HomeModel:
    def __init__(self):
        self._init_model_dict()
        
        
    #通过模型名获取模型种类
    def get_model_type(self, model_name):
        if model_name not in self.model_dict:
            return None
        
        model_type = self.model_dict[model_name]["model_type"]
        return model_type
    
    #加载模型
    def load_translator(self, model_name, lora_input):
        if model_name not in self.model_dict:
            return None
        model_info = self.model_dict[model_name]
        model_type = model_info["model_type"]
        model_path = model_info["model_path"]
        # if "translator" not in model_info:
        #     if model_type == "gguf":
        #         translator = GGUFTranslator(model_path)
        #     if model_type == "safetensors":
        #         translator = SafetensorsTranslator(model_path) 
        #     if model_type == "bin":
        #         translator = BinTranslator(model_path)
        #     if model_type == "M2M100":
        #         translator = M2M100Translator(model_path)
                
        #     model_info["translator"] = translator
        
        # return model_info["translator"]
        if model_type == "gguf":
            translator = GGUFTranslator(model_path)
        if model_type == "safetensors":
            translator = SafetensorsTranslator(model_path) 
        if model_type == "bin":
            translator = BinTranslator(model_path)
        if model_type == "M2M100":
            translator = M2M100Translator(model_path)
        
        #只有safetensors并且不是GPTQ的才可插入lora
        if self.get_model_type(model_name) == "safetensors" and "GPTQ" not in model_name and "gptq" not in model_name:
            lora_dict = self._get_lora_dict(lora_input)
            print(f"lora_dict: {lora_dict}") 
            self._load_lora(translator, lora_dict)
            
        return translator
    
    #底模插入lora微调
    def _load_lora(self, translator, lora_dict:dict):
        base_model = translator.model
        
        # for name, module in base_model.named_modules():
        #     print(name)
            
        total_merged = 0
        for lora, weight in lora_dict.items():
            if lora is None or lora == "":
                continue
            if lora not in self.lora_dict:
                print(f"没有该lora模型: {lora}")
                continue

            info = self.lora_dict[lora]
            model_path = info["model_path"]
            config = PeftConfig.from_pretrained(model_path)
            lora_model = PeftModel.from_pretrained(base_model, model_path, config=config)

            merged = 0

            for name, param in lora_model.named_parameters():
                if "lora_A" in name or "lora_B" in name:
                    try:
                        # 去掉路径中的 "base_model.model.model" 部分
                        name_parts = name.split(".")
                        if name_parts[0] == "base_model":
                            name_parts.pop(0)  # 去掉 "base_model"
                        if name_parts[0] == "model":
                            name_parts.pop(0)  # 去掉 "model"
                        if name_parts[0] == "model":
                            name_parts.pop(0)  # 去掉第二个 "model"

                        # 确保路径从 "model.layers" 开始
                        if name_parts[0] != "model":
                            name_parts.insert(0, "model")

                        module_path = ".".join(name_parts[:-1])
                        param_name = name_parts[-1]

                        # 获取并融合参数
                        target_module = base_model.get_submodule(module_path)
                        base_param = getattr(target_module, param_name)
                        base_param.data += param.data * weight
                        merged += 1
                    except Exception as e:
                        print(f"跳过参数: {name}, 原因: {e}")
                        continue

            total_merged += merged
            print(f"LoRA 模块 {lora} 合并完成，共融合 {merged} 个参数。")
            
            
        if total_merged > 0:
            lora_model.eval() #切换到推理模式
            translator.model = lora_model
            print(f"切换到lora模型，切换为推理模式")
    
    #处理lora输入
    def _get_lora_dict(self, lora_input:str):
        # 处理Lora模型输入并返回模型名和权重数据
        input_list = lora_input.split(',')
        lora_dict = {}

        for input in input_list:
            input = input.strip()  # 去除前后的空白字符

            # 如果包含':'，说明用户输入了权重
            if ':' in input:
                lora, weight = input.split(':')
                try:
                    weight = float(weight)  # 转换权重为浮动数字
                except ValueError:
                    print(f"无效的权重格式: {weight}")
                    continue
            else:
                lora = input
                weight = 1.0  # 默认权重为1.0
                
            lora_dict[lora] = weight
            
        return lora_dict
        
    #获取所有model种类
    def _init_model_dict(self):
        self.model_dict ={}
        self.lora_dict ={}
        model_root = config.MODELS_ROOT
        for root, dirs, files in os.walk(model_root):
            #获取当前目录的相对路径
            relative_path = os.path.relpath(root, model_root)
            # print(relative_path)
            
            if relative_path == "gguf": #每个文件代表一个模型
                for file in files:
                    model_name, ext = os.path.splitext(file)
                    if ext == ".gguf":
                        model_path = os.path.join(root, file)  # 拼接成模型的绝对路径
                        model_info = {"model_path": model_path, "model_type": "gguf"}
                        self.model_dict[model_name] = model_info
                continue
            
            if relative_path == "safetensors": #每个子文件夹是一个模型
                for sub_dir in dirs:
                    model_name = sub_dir
                    model_path = os.path.join(root, sub_dir)  #绝对路径
                    model_info = {"model_path": model_path, "model_type": "safetensors"}
                    self.model_dict[model_name] = model_info
                continue
                
            if relative_path == "bin": #每个子文件夹是一个模型
                for sub_dir in dirs:
                    model_name = sub_dir
                    model_path = os.path.join(root, sub_dir)  #绝对路径
                    model_info = {"model_path": model_path, "model_type": "bin"}
                    self.model_dict[model_name] = model_info
                continue
            
            if relative_path == "M2M100": #每个子文件夹是一个模型
                for sub_dir in dirs:
                    model_name = sub_dir
                    model_path = os.path.join(root, sub_dir)  #绝对路径
                    model_info = {"model_path": model_path, "model_type": "M2M100"}
                    self.model_dict[model_name] = model_info
                continue
            
            if relative_path == "lora":
                for sub_dir in dirs:
                    model_name = sub_dir
                    model_path = os.path.join(root, sub_dir)  #绝对路径
                    model_info = {"model_path": model_path}
                    self.lora_dict[model_name] = model_info
                continue
        