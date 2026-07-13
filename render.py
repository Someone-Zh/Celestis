#!/usr/bin/env python3
"""
渲染目录下所有文件，将 @Template/xxx.md 占位符替换为对应文件内容
输出到 dist 目录（默认）或 skills/name/SKILL.md 格式（--skill 参数）
"""

import argparse
import re
import shutil
from pathlib import Path


def read_file_content(file_path: str) -> str:
    """读取文件内容"""
    with (
        open(file_path, "r", encoding="utf-8") as f
    ):  # 使用上下文管理器以只读模式打开指定路径的文件，指定编码为utf-8，并将文件对象赋值给变量f
        return f.read()  # 读取并返回文件对象f的全部内容


def write_file_content(file_path: str, content: str) -> None:
    """写入文件内容"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def render_content(content: str, base_dir: Path) -> str:
    """
    渲染内容，替换所有 @Template/xxx.md 占位符

    Args:
        content: 原始内容
        base_dir: 基础目录路径

    Returns:
        渲染后的内容
    """
    # 匹配 @Template/xxx.md 格式的占位符
    pattern = r"@Template/([\w_]+\.md)"

    def replace_placeholder(match):
        """替换占位符为对应文件内容"""
        filename = match.group(1)
        template_path = base_dir / "Template" / filename

        if template_path.exists():
            template_content = read_file_content(template_path)
            # 递归渲染，处理模板中可能包含的其他占位符
            return render_content(template_content, base_dir)
        else:
            print(f"警告: 模板文件不存在: {template_path}")
            return match.group(0)  # 保持原样

    # 使用正则替换所有占位符
    rendered_content = re.sub(pattern, replace_placeholder, content)

    return rendered_content


def render_files(source_dir: str = ".", output_dir: str = "dist", skill_format: bool = False) -> None:
    """
    渲染目录下所有文件（不递归）到输出目录

    Args:
        source_dir: 源目录
        output_dir: 输出目录
        skill_format: 是否渲染为 Skill 格式（skills/name/SKILL.md）
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)

    # 创建输出目录
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # 处理源目录下的所有文件（不递归）
    for item in source_path.iterdir():
        # 只处理文件，不处理目录
        if not item.is_file():
            continue

        # 跳过隐藏文件和特殊文件
        if item.name.startswith("."):
            continue

        # 跳过 render.py 和 dist 目录
        if item.name == "render.py" or item.name == "dist":
            continue

        print(f"正在处理: {item.name}")

        # 读取文件内容
        content = read_file_content(item)

        # 渲染内容
        rendered_content = render_content(content, source_path)

        # 确定输出路径
        if skill_format:
            # Skill 格式: skills/{name}/SKILL.md
            skill_name = item.stem  # 文件名（不含扩展名）
            output_file = output_path / skill_name / "SKILL.md"
            output_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            # 默认格式: dist/{filename}
            output_file = output_path / item.name

        # 写入输出目录
        write_file_content(output_file, rendered_content)

        print(f"已完成: {output_file}")

    print(f"\n所有文件已渲染到 {output_dir} 目录")


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description="渲染目录下所有文件，将 @Template/xxx.md 占位符替换为对应文件内容"
    )
    parser.add_argument(
        "--skill",
        action="store_true",
        help="渲染为 Skill 格式（skills/name/SKILL.md）",
    )
    parser.add_argument(
        "--source",
        default=".",
        help="源目录路径（默认为当前目录）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="输出目录路径（默认为 dist，使用 --skill 时默认为 skills）",
    )

    args = parser.parse_args()

    # 确定输出目录
    output_dir = args.output
    if output_dir is None:
        output_dir = "skills" if args.skill else "dist"

    render_files(source_dir=args.source, output_dir=output_dir, skill_format=args.skill)


if __name__ == "__main__":
    main()
