import gradio as gr 
from tkinter import Tk, filedialog
import config


class BatchView:
    def __init__(self):
        self.action_translate = None

    def open(self):
        with gr.Blocks(css="h1 {text-align: center;}") as view:
            gr.Markdown("## 📊 Excel 批量翻译工具")

            with gr.Row():
                with gr.Column(scale=2):

                    with gr.Group():
                        gr.Markdown("### 📁 文件路径设置")
                        input_path = gr.Textbox(label="输入文件路径", placeholder="请选择需要翻译的 Excel 文件", interactive=True)
                        input_path_btn = gr.Button("📂 选择输入文件")

                        # 输出目录控件封装进 Row，便于显示隐藏
                        output_column = gr.Column(visible=True)
                        with output_column:
                            output_dir = gr.Textbox(label="输出目录", placeholder="翻译后的文件将保存在此路径", interactive=True)
                            output_dir_btn = gr.Button("📂 选择输出目录")

                        overwrite = gr.Checkbox(label="📝 是否覆盖原文件", value=False)

                    with gr.Group():
                        gr.Markdown("### 📄 Excel 配置参数")
                        sheet_name = gr.Textbox(label="Sheet 名称", placeholder="例如：Sheet1")
                        input_range = gr.Textbox(label="📥 输入范围", placeholder="C4:C5, C8:C58")
                        output_range = gr.Textbox(label="📤 输出范围", placeholder="D4:D5, D8:D58")

                    translate_btn = gr.Button("🚀 开始批量翻译", variant="primary")
                    result_text = gr.Textbox(label="🧾 翻译日志输出", lines=5, max_lines=20, interactive=False)

            # ✅ 按钮事件绑定
            translate_btn.click(
                fn=self.action_translate,
                inputs=[input_path, sheet_name, input_range, output_range, overwrite, output_dir],
                outputs=result_text
            )

            input_path_btn.click(
                fn=self._get_excel_file_path,
                inputs=input_path,
                outputs=input_path
            )

            output_dir_btn.click(
                fn=self._get_folder_path,
                inputs=output_dir,
                outputs=output_dir
            )

            overwrite.change(
                fn=lambda checked: gr.update(visible=not checked),
                inputs=overwrite,
                outputs=output_column
            )

        return view

    def _get_folder_path(self, folder_path=''):
        if folder_path == '':
            folder_path = config.BATCH_ROOT
        current_folder_path = folder_path
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        folder_path = filedialog.askdirectory(initialdir=folder_path)
        root.destroy()
        return folder_path if folder_path else current_folder_path

    def _get_excel_file_path(self, initial_dir=''):
        if initial_dir == '':
            initial_dir = config.BATCH_ROOT
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="选择Excel",
            filetypes=[("Excel文件", "*.xlsx")]
        )
        root.destroy()
        return file_path
