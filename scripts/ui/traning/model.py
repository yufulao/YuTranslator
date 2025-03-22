import os
import config
from translator.translator_safetensors import SafetensorsTranslator


class TraningModel:
    def __init__(self):
        self._init_model_dict()
        
    #加载模型
    def load_translator(self, model_name):
        model_info = self.model_dict[model_name]
        model_path = model_info["model_path"]
        return SafetensorsTranslator(model_path)
        
    #检索所有safetensors模型
    def _init_model_dict(self):
        self.model_dict ={}
        model_root = config.MODELS_ROOT
        for root, dirs, files in os.walk(model_root):
            #获取当前目录的相对路径
            relative_path = os.path.relpath(root, model_root)
            if relative_path == "safetensors": #每个子文件夹是一个模型
                for sub_dir in dirs:
                    model_name = sub_dir
                    model_path = os.path.join(root, sub_dir)  #绝对路径
                    model_info = {"model_path": model_path}
                    self.model_dict[model_name] = model_info
                continue