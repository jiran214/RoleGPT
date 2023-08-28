import openai
import openai
import config
from utils.api_key_manager import KeyManager, inject_param_decorator

# 限流
key_manager = KeyManager([key for key in config.api_key_list + [config.api_key] if key])
openai.ChatCompletion.create = inject_param_decorator(api_key=key_manager.assign)(openai.ChatCompletion.create)
openai.Embedding.create = inject_param_decorator(api_key=key_manager.assign)(openai.Embedding.create)


# 代理
...


# 测试网络环境
...