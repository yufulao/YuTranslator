import gradio as gr
from core.translator import translate  # 这里调用上面的翻译函数

with gr.Blocks() as demo:
    gr.Markdown("## DeepSeek-R1 8B 翻译系统")
    input_text = gr.Textbox(label="输入英文文本")
    output_text = gr.Textbox(label="翻译结果")
    lang = gr.Dropdown(["French", "Chinese", "German"], label="目标语言", value="Chinese")
    btn = gr.Button("翻译")

    btn.click(translate, inputs=[input_text, lang], outputs=output_text)

demo.launch()
