import openai
import openai as openai
from ratelimit import RateLimitDecorator, limits

import config
from utils.api_key_manager import KeyManager, inject_param_decorator

# 限流
key_manager = KeyManager(config.api_key_list + [config.api_key])
openai.ChatCompletion.create = inject_param_decorator(api_key=key_manager.assign)(openai.ChatCompletion.create)
openai.Embedding.create = inject_param_decorator(api_key=key_manager.assign)(openai.Embedding.create)


# 代理


# 测试网络环境
...