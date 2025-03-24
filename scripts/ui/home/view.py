import gradio
import config

class HomeView:
    def __init__(self):
        self.action_on_btn_click_generate = None
        self.action_get_model_type = None
        self.action_on_lora_models_change = None

    def open(self, model_name_list: list, lora_list: list):
        with gradio.Blocks(css="h1 {text-align: center;}") as view:
            gradio.Markdown("## 🌐 翻译界面")

            if not model_name_list:
                return view

            lora_default = lora_list[0] if lora_list else None

            with gradio.Row(equal_height=True):
                # 左边：输入输出区，占70%
                with gradio.Column(scale=7):
                    input_text = gradio.Textbox(label="📥 输入文本", lines=6, placeholder="请输入待翻译的文本...")
                    output_text = gradio.Textbox(label="📤 翻译结果", lines=6, placeholder="翻译结果将在此显示...")

                # 右边：模型选择和参数设置，占30%
                with gradio.Column(scale=3):
                    target_language = gradio.Dropdown(
                        choices=config.SUPPORTED_LANGUAGES,
                        label="🌍 目标语言",
                        value=config.SUPPORTED_LANGUAGES[0],
                        interactive=True
                    )

                    model_name = gradio.Dropdown(
                        choices=model_name_list,
                        label="🧠 模型选择",
                        value=model_name_list[0],
                        interactive=True
                    )
                    
                    lora_input = gradio.Textbox(
                        label="📝 LoRA模型及权重（逗号分隔）",
                        lines=1,
                        interactive=True,
                        placeholder="lora_model1:0.8, lora_model2:1.0"
                    )

                    lora_dropdown = gradio.Dropdown(
                        choices=lora_list,
                        label="🎯 添加LoRA微调模型",
                        value=lora_default,
                        interactive=True
                    )

                    with gradio.Accordion("⚙️ 高级参数", open=True):
                        params_column_gguf = gradio.Column(visible=False)
                        with params_column_gguf:
                            temperature = gradio.Number(label="🌡️ 随机性 Temperature", value=config.DEFAULT_TEMPERATURE)
                            max_tokens = gradio.Number(label="🔢 最大输出 Tokens", value=config.DEFAULT_MAX_TOKENS)
                            top_p = gradio.Number(label="🎲 多样性 Top P", value=config.DEFAULT_TOP_P)

                        params_column_bin = gradio.Column(visible=False)
                        params_column_safetensor = gradio.Column(visible=False)
                        params_column_m2m100 = gradio.Column(visible=False)

            # 翻译按钮：居中显示
            with gradio.Row():
                btn_translate = gradio.Button("🚀 开始翻译", elem_id="center-button", variant="primary")
                
                
            # 缓存数据
            from ui.main_controller import MainController
            state = MainController().state
            #初始化了value的dropdown必须传入input，直接使用value默认值取得的都是默认值
            home_info = {
                "target_language": config.SUPPORTED_LANGUAGES[0],
                "model_name": model_name_list[0],
                "lora_input": "",
                "temperature": temperature.value,
                "max_tokens": max_tokens.value,
                "top_p": top_p.value,
            }
            state["home"] = home_info
            

            # 事件处理逻辑
            def _on_value_change_target_language(value): home_info["target_language"] = value
            
            def _on_value_change_model_name(value):
                home_info["model_name"] = value
                model_type = self.action_get_model_type(value)
                return {
                    params_column_gguf: gradio.update(visible=(model_type == "gguf")),
                    params_column_bin: gradio.update(visible=(model_type == "bin")),
                    params_column_safetensor: gradio.update(visible=(model_type == "safetensors")),
                    params_column_m2m100: gradio.update(visible=(model_type == "m2m100")),
                }

            def _on_value_change_lora_dropdown(dropdown, text):
                fixed_text = self._process_lora_input(dropdown, text)
                home_info["lora_input"] = fixed_text
                return fixed_text

            def _on_value_change_temperature(): home_info["temperature"] = temperature.value
            def _on_value_change_max_tokens(): home_info["max_tokens"] = max_tokens.value
            def _on_value_change_top_p(): home_info["top_p"] = top_p.value

            # 事件绑定
            target_language.change(_on_value_change_target_language, inputs=target_language)
            model_name.change(_on_value_change_model_name, inputs=model_name,
                              outputs=[params_column_gguf, params_column_bin, params_column_safetensor, params_column_m2m100])
            lora_dropdown.select(_on_value_change_lora_dropdown, inputs=[lora_dropdown, lora_input], outputs=lora_input)
            temperature.change(_on_value_change_temperature)
            max_tokens.change(_on_value_change_max_tokens)
            top_p.change(_on_value_change_top_p)

            btn_translate.click(
                fn=self.action_on_btn_click_generate,
                inputs=[
                    input_text, target_language, model_name, lora_input,
                    temperature, max_tokens, top_p
                ],
                outputs=output_text
            )

        return view

    def _process_lora_input(self, lora_dropdown: str, lora_input: str) -> str:
        if not lora_input:
            return f"{lora_dropdown}:1.0"
        return f"{lora_input}, {lora_dropdown}:1.0"
