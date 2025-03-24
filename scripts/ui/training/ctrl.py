from ui.training.model import TrainingModel
from ui.training.view import TrainingView
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments, Trainer
from datasets import load_dataset
import torch

class TrainingCtrl:
    def __init__(self):
        self._model = TrainingModel()
        self._view = TrainingView()
        self._view.action_start_training = self.start_training
        
    def open(self):
        return self._view.open(list(self._model.model_dict.keys()))
    
    #训练
    def start_training(self, model_name, lr, batch_size, epochs, train_data, output_dir, weights_dir):
        if not train_data or not output_dir or not weights_dir:
            return
        batch_size = int(batch_size)
        
        lora_config = LoraConfig(
            r=8,  # LoRA 低秩维度（控制额外参数量）
            lora_alpha=16,
            lora_dropout=0.05,
            target_modules=["q_proj", "v_proj"],  # 指定要插入 LoRA 的层（视模型结构而定）
            bias="none"
        )
        
        training_args = TrainingArguments(
            learning_rate=lr,
            per_device_train_batch_size=batch_size,
            num_train_epochs=epochs,
            logging_steps=10,
            output_dir=weights_dir,
            save_strategy="epoch",
            report_to="none"
        )
        
        #GPTQ的不支持lora
        if "GPTQ" in model_name or "gptq" in model_name:
            return "GPTQ量化的safetensors不支持lora"
        
        translator = self._model.load_translator(model_name)
        if translator == None:
            return 
        model = get_peft_model(translator.model, lora_config)
        print("Lora适配层已插入")
        model.print_trainable_parameters()
    
        #处理数据
        dataset = load_dataset("json", data_files=train_data)
        dataset = dataset.map(lambda examples: self._preprocess_function(examples, translator.tokenizer), batched=True)
        print("First batch after preprocessing:")
        print("Input IDs:", dataset["train"][0]["input_ids"])
        print("Labels:", dataset["train"][0]["labels"])
        print("Attention mask:", dataset["train"][0]["attention_mask"])
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset["train"]
        )
        
        model.save_pretrained(output_dir)
        trainer.train()
        print("Lora训练完成，权重已保存")
        return "LoRA训练完成，权重已保存"
    
    #处理数据集
    def _preprocess_function(self, examples, tokenizer):
        inputs = tokenizer(
            examples["input"],
            truncation=True,
            padding=True,
            max_length=512  # 设置一个固定的最大长度（根据数据调整）
        )
        
        # 对 output 进行 tokenization，并确保长度与 input 一致
        outputs = tokenizer(
            examples["output"],
            truncation=True,
            padding=True,
            max_length=len(inputs["input_ids"][0])  # 动态截断到 input 的长度
        )
        
        # 将 output 的 input_ids 作为 labels
        inputs["labels"] = outputs["input_ids"]
        
        # 打印形状以验证
        print("Input IDs shape:", torch.tensor(inputs["input_ids"]).shape)
        print("Labels shape:", torch.tensor(inputs["labels"]).shape)
        print("Attention mask shape:", torch.tensor(inputs["attention_mask"]).shape)
        
        return inputs
