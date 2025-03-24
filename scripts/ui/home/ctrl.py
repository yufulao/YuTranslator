from ui.home.model import HomeModel
from ui.home.view import HomeView


class HomeCtrl:
    def __init__(self):
        self._model = HomeModel()
        self._view = HomeView()
        self._bind_event()
        # print(self._model.model_dict)

    #打开界面
    def open(self):
        model_name_list = list(self._model.model_dict.keys())
        lora_list = list(self._model.lora_dict.keys())
        return self._view.open(model_name_list, lora_list)
    
    #获取translator
    def get_translator(self, model_name, lora_input):
        return self._model.load_translator(model_name, lora_input)
    
    #外部使用Home界面的参数进行翻译
    def translate(self, input_text, target_language, model_name, lora_input, *arg)->str:
        print(f"translator params:\n  input_text: {input_text}\n  target_language: {target_language}\n  "  +
              f"model_name: {model_name}\n  lora_input: {lora_input}\n  *arg: {arg}")
        translator = self._model.load_translator(model_name, lora_input)
        if not translator:
            print("没有translator")
            return "没有translator"
        return translator.generate_text(input_text, target_language, *arg)
    
    #通过translator翻译
    def translate_by_translator(self, translator, input_text, target_language, *arg):
        if not translator:
            print("没有translator")
            return "没有translator"
        return translator.generate_text(input_text, target_language, *arg)  
        
    #绑定事件
    def _bind_event(self):
        self._view.action_on_btn_click_generate = self._on_btn_click_generate
        self._view.action_get_model_type = self._model.get_model_type
    
    #当点击翻译按钮时
    def _on_btn_click_generate(self, input_text, target_language, model_name, lora_input, *arg):
        output = self.translate(input_text, target_language, model_name, lora_input, *arg)
        # print(f"翻译结果: {output}")
        return output

