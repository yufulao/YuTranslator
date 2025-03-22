import gradio as gr
from ui.home.ctrl import HomeCtrl
from ui.traning.ctrl import TraningCtrl
from ui.evaluate.ctrl import EvaluateCtrl

class MainController:
    _instance = None  # 单例引用
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MainController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        #单例
        if self._initialized:
            return
        self._initialized = True
        self.state = {}
        self.on_tab_change = []
        
        self.home_ctrl = HomeCtrl()
        self.traning_ctrl = TraningCtrl()
        self.evaluate_ctrl = EvaluateCtrl()
    
    def launch(self):
        with gr.Blocks() as app:
            with gr.Tabs() as tabs:
                with gr.TabItem("主界面"):
                    self.home_ctrl.open()
                
                # with gr.TabItem("微调训练"):
                #     self.traning_ctrl.open()
                
                with gr.TabItem("准确度评估"):
                    self.evaluate_ctrl.open()
                    
        app.launch()
        
