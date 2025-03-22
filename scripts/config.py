# 默认参数
import os

DEFAULT_TEMPERATURE = 0.1 #随机性
DEFAULT_MAX_TOKENS = 512 #最大输出token
DEFAULT_TOP_P = 0.9 #多样性
# DEFAULT_NUM_OUTPUTS = 1 #输出结果个数
# DEFAULT_BATCH_SIZE = 1 #批处理大小

SCRIPTS_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_ROOT)
LIB_DIR = os.path.join(SCRIPTS_ROOT, "lib")
MODELS_ROOT = os.path.join(PROJECT_ROOT, "models")
TRAINING_ROOT = os.path.join(PROJECT_ROOT, "training")
# print(PROJECT_ROOT)
# print(SCRIPTS_ROOT)
# print(LIB_DIR)
# print(MODELS_ROOT)

# MODEL_PATH = "../models/safetensors/DeepSeek-R1-1.5B"
# "DeepSeek-R1-Distill-Llama-8B-Q3_K_L.gguf" 可以
# "t5_translate_en_ru_zh_small_1024" 垃圾
# "DeepSeek-R1-8B" 用不起
# "DeepSeek-R1-1.5B"
# "nllb-200-distilled-600M" 垃圾
# "m2m100_12B" 垃圾
# "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf" 差不多
# "DeepSeek-R1-Distill-Qwen-1.5B-IQ2_M.gguf" 弱智

# SUPPORTED_LANGUAGES = [
#     "eng_Latn",
#     "zho_Hans",
#     "zho_Hant",
#     "jpn_Jpan",
#     "deu_Latn",
# ]

SUPPORTED_LANGUAGES = ["English", "Chinese", "Japanese", "French", "German", "Spanish"]

# 语言映射NLLB语言代码
LANG_MAP = {
    "en": "eng_Latn",
    "zh-cn": "zho_Hans",
    "zh-tw": "zho_Hant",
    "ja": "jpn_Jpan",
    "de": "deu_Latn",
}

M2M100_SUPPORTED_LANGUAGES = [
    "en",
    "zh",
    "ja",
    "de",
]

# BERTScore F1评估可选语言
BERT_SCORE_LANGUAGES = ["zh", "en", "ja", "de", "fr", "es", "ko", "ru", "pt"]


