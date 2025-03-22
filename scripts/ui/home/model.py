import os
import config
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
    
    def translate(self, input_text, target_language, model_name, *arg):
        translator = self._load_translator(model_name)
        if not translator:
            return ""
        return translator.generate_text(input_text, target_language, *arg)
    
    #加载模型
    def _load_translator(self, model_name):
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
            return GGUFTranslator(model_path)
        if model_type == "safetensors":
            return SafetensorsTranslator(model_path) 
        if model_type == "bin":
            return BinTranslator(model_path)
        if model_type == "M2M100":
            return M2M100Translator(model_path)
        
    #获取所有model种类
    def _init_model_dict(self):
        self.model_dict ={}
        model_root = config.MODELS_ROOT
        for root, dirs, files in os.walk(model_root):
            #获取当前目录的相对路径
            relative_path = os.path.relpath(root, model_root)
            
            if relative_path == "bin": #每个子文件夹是一个模型
                for sub_dir in dirs:
                    model_name = sub_dir
                    model_path = os.path.join(root, sub_dir)  #绝对路径
                    model_info = {"model_path": model_path, "model_type": "bin"}
                    self.model_dict[model_name] = model_info
                continue
                
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
            
            if relative_path == "M2M100": #每个子文件夹是一个模型
                for sub_dir in dirs:
                    model_name = sub_dir
                    model_path = os.path.join(root, sub_dir)  #绝对路径
                    model_info = {"model_path": model_path, "model_type": "M2M100"}
                    self.model_dict[model_name] = model_info
                continue
        