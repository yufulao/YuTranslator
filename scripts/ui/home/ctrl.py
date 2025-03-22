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
        model_name_list = self._model.model_dict.keys()
        return self._view.open(model_name_list)
        
    #绑定事件
    def _bind_event(self):
        self._view.action_on_btn_click_generate = self._on_btn_click_generate
        self._view.action_get_model_type = self._model.get_model_type
    
    #当点击翻译按钮时
    def _on_btn_click_generate(self, input_text, target_language, model_name, *arg):
        # print(arg)
        output = self._model.translate(input_text, target_language, model_name, *arg)
        # print(f"翻译结果: {output}")
        return output


