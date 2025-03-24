import gradio as gr
from tkinter import Tk, filedialog
import config

class TrainingView:
    def __init__(self):
        self.action_start_training = None

    def open(self, model_list: list):
        with gr.Blocks(css="h1 {text-align: center;}") as view:
            gr.Markdown("## 🔧 LoRA 微调训练")

            with gr.Row():
                # 左列：参数配置
                with gr.Column(scale=6):
                    model_path = gr.Dropdown(choices=model_list, label="🧠 选择底模", value=model_list[0] if model_list else None)
                    learning_rate = gr.Number(value=0.001, label="📈 学习率")
                    batch_size = gr.Number(value=4, label="📦 Batch Size")
                    num_epochs = gr.Number(value=3, label="🔁 Epoch 数")

                # 右列：路径选择
                with gr.Column(scale=6):
                    train_data = gr.Textbox(label="📁 训练集路径", interactive=True)
                    train_data_btn = gr.Button("📂 选择训练集")

                    output_dir = gr.Textbox(label="📁 输出目录", interactive=True)
                    output_dir_btn = gr.Button("📂 选择输出目录")

                    weights_dir = gr.Textbox(label="📂 中间产物目录", interactive=True)
                    weights_dir_btn = gr.Button("📂 选择中间产物目录")

            # 按钮居中
            with gr.Row():
                btn_train = gr.Button("🚀 开始训练", elem_id="center-button", variant="primary")

            # 日志区
            train_output = gr.Textbox(label="📋 训练日志输出", lines=10, interactive=False)

            # 绑定路径选择
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

            # 点击开始训练
            btn_train.click(
                fn=self.action_start_training,
                inputs=[
                    model_path, learning_rate, batch_size, num_epochs,
                    train_data, output_dir, weights_dir
                ],
                outputs=train_output
            )

        return view

    def _get_folder_path(self, folder_path=''):
        if folder_path == '':
            folder_path = config.TRAINING_ROOT
        current_folder_path = folder_path
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        folder_path = filedialog.askdirectory(initialdir=folder_path)
        root.destroy()
        return folder_path if folder_path else current_folder_path

    def _get_json_file_path(self, initial_dir=''):
        if initial_dir == '':
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
