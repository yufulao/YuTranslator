import gradio as gr
from ui.home.ctrl import HomeCtrl
from ui.traning.ctrl import TraningCtrl

class MainController:
    def __init__(self):
        self.home_ctrl = HomeCtrl()
        self.traning_ctrl = TraningCtrl()
    
    def launch(self):
        with gr.Blocks() as app:
            with gr.Tabs():
                with gr.TabItem("主界面"):
                    self.home_ctrl.open()
                
                with gr.TabItem("微调训练"):
                    self.traning_ctrl.open()
        
        app.launch()
