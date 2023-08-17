import openai
from ratelimit import RateLimitDecorator


# 限流
openai.ChatCompletion.create = RateLimitDecorator(calls=3, period=1, raise_on_limit=False)(openai.ChatCompletion.create)
openai.Embedding.create = RateLimitDecorator(calls=3, period=1, raise_on_limit=False)(openai.Embedding.create)


# 代理


# 测试网络环境
...