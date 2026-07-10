import os

from dotenv import load_dotenv
from openai import OpenAI


class LLMClient:
    """
    统一封装大模型调用。

    当前版本默认调用 Kimi API。
    后续如果要接入 OpenAI、DeepSeek、Qwen，只需要扩展这个文件。
    """

    def __init__(self):
        load_dotenv()

        self.provider = os.getenv("MODEL_PROVIDER", "kimi").lower()

        if self.provider == "kimi":
            api_key = os.getenv("MOONSHOT_API_KEY")
            base_url = os.getenv("KIMI_BASE_URL", "https://api.moonshot.ai/v1")
            model = os.getenv("KIMI_MODEL", "kimi-k2.6")

            if not api_key:
                raise ValueError("没有读取到 MOONSHOT_API_KEY，请检查 .env 文件。")

            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )
            self.model = model
        else:
            raise ValueError(f"暂不支持的模型提供方：{self.provider}")

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if content is None:
            return ""

        return content