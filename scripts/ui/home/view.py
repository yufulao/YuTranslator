import gradio
import config

class HomeView:
    def __init__(self):
        self.action_on_btn_click_generate = None #(model_name, **params)->generated_text
        self.action_get_model_type = None #(model_name)->model_type

    def open(self, model_name_list):
        with gradio.Blocks() as view:
        
            input_text = gradio.Textbox(label="输入文本", lines=3)
            target_language = gradio.Dropdown(list(config.SUPPORTED_LANGUAGES), label="目标语言", value="English")
        
            #模型选择框
            model_name_dropdown = gradio.Dropdown(
                choices = list(model_name_list), 
                label="(选择模型)", 
                interactive=True
            )
            
            #参数列表
            with gradio.Column(visible=False) as params_column_gguf:
                temperature = gradio.Number(label="随机性temperature", value=config.DEFAULT_TEMPERATURE)
                max_tokens = gradio.Number(label="最大输出max tokens", value=config.DEFAULT_MAX_TOKENS)
                top_p = gradio.Number(label="多样性top P", value=config.DEFAULT_TOP_P)
            with gradio.Column(visible=False) as params_column_bin:
                pass
            with gradio.Column(visible=False) as params_column_safetensor:
                pass
            with gradio.Column(visible=False) as params_column_m2m100:
                pass
            
            #更新参数
            def _update_params(model_name):
                model_type = self.action_get_model_type(model_name)
                return {
                    params_column_gguf:gradio.update(visible=(model_type == "gguf")),
                    params_column_bin:gradio.update(visible=(model_type == "bin")),
                    params_column_safetensor:gradio.update(visible=(model_type == "safetensors")),
                    params_column_m2m100:gradio.update(visible=(model_type == "m2m100")),
                }
            
            model_name_dropdown.change(
                fn=_update_params, 
                inputs=model_name_dropdown,
                outputs=[params_column_gguf, params_column_bin, params_column_safetensor, params_column_m2m100]
            )
            
            output_text = gradio.Textbox(label="翻译结果", lines=3)
            
            #翻译按钮
            btn_translate = gradio.Button("翻译")
            
            btn_translate.click(
                fn=self.action_on_btn_click_generate, 
                inputs=[
                    input_text, target_language, model_name_dropdown,
                    temperature, max_tokens, top_p, 
                ],
                outputs=output_text
            )
            
        return view
        