from pathlib import Path

from llm_client import LLMClient
from tools.file_reader import read_file
from tools.skill_loader import load_skill


TASKS = {
    "1": {
        "title": "论文终稿检查",
        "skill": "paper-final-check-skill",
        "output_suffix": "论文检查结果",
        "task_prompt": (
            "请按照 skill 的要求检查这份材料。重点关注方法、实验和结论是否对应，"
            "同时检查公式编号、图表引用、符号统一、摘要缩写和可提交性。"
        ),
    },
    "2": {
        "title": "课程汇报内容生成",
        "skill": "course-ppt-content-skill",
        "output_suffix": "课程汇报内容",
        "task_prompt": (
            "请按照 skill 的要求，根据这份材料生成 5 分钟课程汇报 PPT 内容和口头汇报稿。"
            "页面文字不要太多，内容要有汇报主线、页面安排、图示建议和时间分配。"
        ),
    },
}


def save_result(input_path: str, suffix: str, content: str) -> Path:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    input_name = Path(input_path).stem
    output_path = output_dir / f"{input_name}_{suffix}.md"

    output_path.write_text(content, encoding="utf-8")
    return output_path


def build_system_prompt(skill_text: str) -> str:
    return f"""
你是一个本地学术材料处理 agent。

你必须严格遵守下面的 skill 说明：

{skill_text}

通用规则：
1. 所有结论必须来自用户提供的材料。
2. 不要编造页码、公式编号、图表编号、实验数据或文件内容。
3. 如果材料读取不完整，需要明确说明“从现有材料无法确认”。
4. 输出使用中文，表达自然，不要使用夸张形容词。
5. 输出内容要适合保存为 Markdown 文件。
"""


def main():
    print("academic-agent")
    print("请选择任务：")

    for key, value in TASKS.items():
        print(f"{key}. {value['title']}")

    choice = input("请输入任务编号：").strip()

    if choice not in TASKS:
        print("任务编号不正确。")
        return

    file_path = input("请输入文件路径：").strip().strip('"')

    try:
        task = TASKS[choice]

        print("\n正在读取 skill...")
        skill_text = load_skill(task["skill"])

        print("正在读取文件...")
        document_text = read_file(file_path)

        if not document_text.strip():
            print("文件内容为空，可能是扫描版 PDF 或暂不支持的格式。")
            return

        print("正在调用 Kimi API...")
        llm = LLMClient()

        system_prompt = build_system_prompt(skill_text)

        user_prompt = f"""
任务要求：
{task["task_prompt"]}

待处理材料内容如下：
{document_text}
"""

        result = llm.chat(system_prompt=system_prompt, user_prompt=user_prompt)

        output_path = save_result(
            input_path=file_path,
            suffix=task["output_suffix"],
            content=result,
        )

        print("\n处理完成。")
        print(f"输出文件：{output_path}")

    except Exception as error:
        print("\n运行失败。")
        print(f"错误信息：{error}")


if __name__ == "__main__":
    main()