from llm_client import LLMClient


def main():
    llm = LLMClient()

    result = llm.chat(
        system_prompt="你是一个中文助手，请用简洁自然的语言回答。",
        user_prompt="请用一句话说明什么是 agent。"
    )

    print(result)


if __name__ == "__main__":
    main()