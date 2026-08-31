# Model Configurations

```python
class _SaferChatOpenAI(ChatOpenAI):
    ...

model = _SaferChatOpenAI(
    api_key=...,
    base_url="https://api.siliconflow.cn/v1",
    model="<vision-model-name>",
    timeout=300,
    max_retries=3,
    max_tokens=32768,
    temperature=0.7,
    # top_p=0.95,
    # frequency_penalty=0.0,
    # presence_penalty=1.5,
    # seed=_seed,
    extra_body={
        # "top_k": 20,
        # "repetition_penalty": 1.05,
        # "min_p": 0.0,
        # "enable_thinking": True,
        # "thinking_budget": 32768,
    },
)
```
