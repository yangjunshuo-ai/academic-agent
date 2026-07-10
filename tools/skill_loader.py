from pathlib import Path


def load_skill(skill_name: str) -> str:
    """
    根据 skill 名称读取对应的 SKILL.md 文件。

    参数：
        skill_name: skill 文件夹名称，例如 paper-final-check-skill

    返回：
        SKILL.md 的文本内容
    """
    skill_path = Path("skills") / skill_name / "SKILL.md"

    if not skill_path.exists():
        raise FileNotFoundError(f"没有找到 skill 文件：{skill_path}")

    return skill_path.read_text(encoding="utf-8")
