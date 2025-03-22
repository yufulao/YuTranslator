# ui/evaluate/ctrl.py
from ui.evaluate.model import EvaluateModel
from ui.evaluate.view import EvaluateView

class EvaluateCtrl:
    def __init__(self):
        self._model = EvaluateModel()
        self._view = EvaluateView()
        self._view.action_evaluate = self.evaluate
        from ui.main_controller import MainController
        self._view.action_back_translate = MainController().home_ctrl.translate

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