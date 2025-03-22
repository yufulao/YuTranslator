import gradio
import config

class HomeView:
    def __init__(self):
        self.action_on_btn_click_generate = None #(model_name, **params)->generated_text
        self.action_get_model_type = None #(model_name)->model_type

    def open(self, model_name_list:list):
        with gradio.Blocks() as view:
            gradio.Markdown("# 翻译")
            if model_name_list == None or len(model_name_list) == 0:
                return view
        
        
            input_text = gradio.Textbox(label="输入文本", lines=3)
            target_language = gradio.Dropdown(list(config.SUPPORTED_LANGUAGES), label="目标语言", value="English")
            
            #模型选择框
            model_name = gradio.Dropdown(
                choices = list(model_name_list), 
                label="(选择模型)", 
                value=model_name_list[0],
                interactive=True,
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
            
            #缓存数据
            from ui.main_controller import MainController
            state = MainController().state
            home_info = {
                "model_name": model_name.value,
                "temperature": temperature.value,
                "max_tokens": max_tokens.value,
                "top_p": top_p.value,
            }
            state["home"] = home_info
            
            #事件
            def _on_value_change_model_name(value):
                home_info["model_name"] = value
                model_type = self.action_get_model_type(value)
                return {
                    params_column_gguf:gradio.update(visible=(model_type == "gguf")),
                    params_column_bin:gradio.update(visible=(model_type == "bin")),
                    params_column_safetensor:gradio.update(visible=(model_type == "safetensors")),
                    params_column_m2m100:gradio.update(visible=(model_type == "m2m100")),
                }
            def _on_value_change_temperature():
                home_info["temperature"] = temperature.value
                
            def _on_value_change_max_tokens():
                home_info["max_tokens"] = max_tokens.value
                
            def _on_value_change_top_p():
                home_info["top_p"] = top_p.value
                
                
            #订阅
            model_name.change(
                fn=_on_value_change_model_name, 
                inputs=model_name,
                outputs=[params_column_gguf, params_column_bin, params_column_safetensor, params_column_m2m100]
            )
            
            temperature.change(
                fn=_on_value_change_temperature, 
            )
            
            max_tokens.change(
                fn=_on_value_change_max_tokens, 
            )
            
            top_p.change(
                fn=_on_value_change_top_p, 
            )
            
            output_text = gradio.Textbox(label="翻译结果", lines=3)
            
            #翻译按钮
            btn_translate = gradio.Button("翻译")
            
            btn_translate.click(
                fn=self.action_on_btn_click_generate, 
                inputs=[
                    input_text, target_language, model_name,
                    temperature, max_tokens, top_p, 
                ],
                outputs=output_text
            )
            
        return view
        
        