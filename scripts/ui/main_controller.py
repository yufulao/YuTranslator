import gradio as gr
from ui.home.ctrl import HomeCtrl
from ui.index.index import _custom_css, _landing_html
from ui.training.ctrl import TrainingCtrl
from ui.evaluate.ctrl import EvaluateCtrl
from ui.batch.ctrl import BatchCtrl


class MainController:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(MainController, cls).__new__(cls)
            cls.instance._initialized = False
        return cls.instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.state = {}

        self.home_ctrl = HomeCtrl()
        self.traning_ctrl = TrainingCtrl()
        self.evaluate_ctrl = EvaluateCtrl()
        self.batch_ctrl = BatchCtrl()

    def launch(self):
        with gr.Blocks(css=_custom_css()) as app:
            with gr.Tabs(elem_id="main-tabs") as tabs:
                with gr.TabItem("首页"):
                    gr.HTML(_landing_html())

                with gr.TabItem("翻译"):
                    self.home_ctrl.open()

                with gr.TabItem("微调训练"):
                    self.traning_ctrl.open()

                with gr.TabItem("翻译评估"):
                    self.evaluate_ctrl.open()
                    
                with gr.TabItem("批量翻译"):
                    self.batch_ctrl.open()

        app.launch()


if __name__ == "__main__":
    MainController().launch()
