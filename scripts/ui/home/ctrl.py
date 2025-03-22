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
        return self._view.open(model_name_list)
    
    #外部使用Home界面的参数进行翻译
    def translate(self, input_text, target_language)->str:
        from ui.main_controller import MainController
        state = MainController().state
        if "home" not in state:
            return "未设置翻译界面参数"
        home_info = state["home"]
        model_name = home_info["model_name"]
        temperature = home_info["temperature"]
        max_tokens = home_info["max_tokens"]
        top_p = home_info["top_p"]
        return self._on_btn_click_generate(input_text, target_language, model_name, temperature, max_tokens, top_p)
        
    #绑定事件
    def _bind_event(self):
        self._view.action_on_btn_click_generate = self._on_btn_click_generate
        self._view.action_get_model_type = self._model.get_model_type
    
    #当点击翻译按钮时
    def _on_btn_click_generate(self, input_text, target_language, model_name, *arg):
        print(f"translator params:\n  input_text: {input_text}\n  target_language: {target_language}\n  model_name: {model_name}\n  *arg: {arg}")
        output = self._model.translate(input_text, target_language, model_name, *arg)
        # print(f"翻译结果: {output}")
        return output

