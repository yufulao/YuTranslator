# ui/evaluate/ctrl.py
from ui.evaluate.model import EvaluateModel
from ui.evaluate.view import EvaluateView

class EvaluateCtrl:
    def __init__(self):
        self._model = EvaluateModel()
        self._view = EvaluateView()
        self._view.action_evaluate = self.evaluate
        self._view.action_back_translate = self._on_btn_click_back_translate

    def open(self):
        return self._view.open()

    def evaluate(self, algorithm:str, prediction:str, reference:str, lang=None):
        if algorithm == None or prediction == None or reference == None:
            return "error：参数不完整"
        predictions = [prediction]
        #处理多个参考翻译
        references = [r.strip() for r in reference.split("\n") if r.strip()]
        references = [references]  # 将 references 转为二维列表
        result = self._model.evaluate(algorithm, predictions, references, lang)
        return result
    
    #点击回译btn
    def _on_btn_click_back_translate(self, input_text, target_language):
        from ui.main_controller import MainController
        state = MainController().instance.state
        if "home" not in state:
            return "未设置翻译界面参数"
        home_info = state["home"]
        model_name = home_info["model_name"]
        lora_input = home_info["lora_input"]
        temperature = home_info["temperature"]
        max_tokens = home_info["max_tokens"]
        top_p = home_info["top_p"]
        arg = (temperature, max_tokens, top_p)
        return MainController.instance.home_ctrl.translate(input_text, target_language, model_name, lora_input, *arg)