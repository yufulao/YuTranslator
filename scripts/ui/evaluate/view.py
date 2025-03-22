import gradio as gr
import config

class EvaluateView:
    def __init__(self):
        self.action_evaluate = None
        self.action_back_translate = None

    def open(self):
        with gr.Blocks() as view:
            gr.Markdown("# 翻译评估")

            #界面
            algorithm = gr.Dropdown(choices=["BLEU", "CHRF", "METEOR", "BERTScore F1"], label="选择评估算法")
            lang_input = gr.Dropdown(choices=config.BERT_SCORE_LANGUAGES, label="评估语言", visible=False)
            toggle_back_translation = gr.Checkbox(label="使用回译评估", value=False)
            prediction = gr.Textbox(label="翻译结果", lines=5)
            references = gr.Textbox(label="参考翻译", placeholder="每行一个参考翻译", lines=5, interactive=True)
            with gr.Column(visible=False) as params_use_back:
                source = gr.Textbox(label="未翻译原文", lines=5)
                back_lang = gr.Dropdown(label="回译目标语言", choices=config.SUPPORTED_LANGUAGES, value="Chinese")
                btn_back_translate = gr.Button("执行回译")
                back_references = gr.Textbox(label="回译结果", lines=5)
                
            btn_evaluate = gr.Button("开始评估")
            output = gr.Textbox(label="评估结果", lines=3)


            #事件
            def toggle_lang_input(alg):
                return gr.update(visible=(alg == "BERTScore F1"))
            
            def toggle_back_translation_change(checked):
                return {
                    params_use_back:gr.update(visible=checked),
                    references:gr.update(visible=not checked)
                }
            
            def on_btn_click_evaluate(checked, algorithm, source, back_references, prediction, references, lang_input):
                if self.action_evaluate == None:
                    return "空回调"
                
                # print(checked)
                if checked:
                    return self.action_evaluate(algorithm, source, back_references, lang_input)
                
                return self.action_evaluate(algorithm, prediction, references, lang_input)

            #订阅
            algorithm.change(toggle_lang_input, inputs=algorithm, outputs=lang_input)
            
            toggle_back_translation.change(
                toggle_back_translation_change, 
                inputs=toggle_back_translation, 
                outputs=[params_use_back, references]
            )
            
            btn_back_translate.click(
                fn=self.action_back_translate,
                inputs=[prediction, back_lang],
                outputs=back_references
            )
            
            btn_evaluate.click(
                fn=on_btn_click_evaluate,
                inputs=[toggle_back_translation, algorithm, source, back_references, prediction, references, lang_input],
                outputs=output
            )

        return view