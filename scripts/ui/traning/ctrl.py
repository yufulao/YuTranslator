from ui.traning.model import TraningModel
from ui.traning.view import TraningView
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments, Trainer
from datasets import load_dataset
import config


class TraningCtrl:
    def __init__(self):
        self._model = TraningModel()
        self._view = TraningView()
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
        
        
        translator = self._model.load_translator(model_name)
        model = get_peft_model(translator.model, lora_config)
        print("Lora适配层已插入")
        model.print_trainable_parameters()
    
        #处理数据
        dataset = load_dataset("json", data_files=train_data)
        dataset = dataset.map(lambda examples: self._preprocess_function(examples, translator.tokenizer), batched=True)
        
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
        #处理输入输出
        model_inputs = tokenizer(examples["input"], truncation=True, padding=True)
        labels = tokenizer(examples["output"], truncation=True, padding=True).input_ids
        #由于Transformer模型的目标是通过labels来计算损失，所以我们需要将输出标记为labels
        #由于模型生成时会将pad_token_id视为负数，因此需要去除padding部分
        model_inputs["labels"] = labels
        return model_inputs
