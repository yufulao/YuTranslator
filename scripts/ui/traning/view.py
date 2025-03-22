import gradio as gr
import os
import sys
from tkinter import Tk, filedialog
import config

class TraningView:
    def __init__(self):
        self.action_start_training = None

    def open(self, model_list:list):
        with gr.Blocks() as view:
            gr.Markdown("# LoRA 训练")
            
            model_path = gr.Dropdown(choices=model_list, label="选择底模")
            train_data = gr.Textbox(label="训练集")
            train_data_btn = gr.Button("选择训练集")
            output_dir = gr.Textbox(label="输出目录")
            output_dir_btn = gr.Button("选择输出目录")
            weights_dir = gr.Textbox(label="训练中间产物输出目录")
            weights_dir_btn = gr.Button("选择训练中间产物输出目录")
            
            learning_rate = gr.Number(value=0.001, label="学习率")
            batch_size = gr.Number(value=4, label="Batch Size")
            num_epochs = gr.Number(value=3, label="训练 Epoch")

            btn_train = gr.Button("开始训练")
            train_output = gr.Textbox(label="训练日志", lines=5)

            train_data_btn.click(
                fn=self._get_json_file_path,
                inputs=train_data,
                outputs=train_data
            )
            
            output_dir_btn.click(
                fn=self._get_folder_path,
                inputs=output_dir,
                outputs=output_dir
            )
            
            weights_dir_btn.click(
                fn=self._get_folder_path,
                inputs=weights_dir,
                outputs=weights_dir
            )

            # 点击开始训练按钮
            btn_train.click(
                fn=self.action_start_training,
                inputs=[model_path, learning_rate, batch_size, num_epochs, train_data, output_dir, weights_dir],
                outputs=train_output
            )

        return view
    
    #tk选择文件夹
    def _get_folder_path(self, folder_path=''):
        if folder_path =='':
            folder_path = config.TRAINING_ROOT
        current_folder_path = folder_path #记录当前路径
        initial_dir = folder_path if folder_path else os.getcwd() #选择框的初始目录
        
        root = Tk()
        root.withdraw() #隐藏Tkinter主窗口
        root.wm_attributes('-topmost', 1)  #置顶
        folder_path = filedialog.askdirectory(initialdir=initial_dir) #选择目录
        root.destroy()

        #如果用户未选择任何文件夹，则返回原路径
        return folder_path if folder_path else current_folder_path
    
    #tk选择文件
    def _get_json_file_path(self, initial_dir=''):
        if initial_dir =='':
            initial_dir = config.TRAINING_ROOT
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir, 
            title="选择JSON训练集",
            filetypes=[("JSON文件", "*.json")]
        )
        root.destroy()
        return file_path