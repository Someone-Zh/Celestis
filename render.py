#!/usr/bin/env python3
"""
渲染目录下所有技能源文件，将 @Template/xxx.md 占位符替换为对应文件内容，
并将 {{@path.to.value}} 替换为 Template/vars.json 中的变量值。
输出到 dist 目录（默认）或 skills/name/SKILL.md 格式（--skill 参数）
只渲染 init.md / create.md / apply.md / fix.md；README.md 等其他文件会被跳过。
"""

import argparse
import json
import re
import shutil
from pathlib import Path

# 只有这些文件会渲染为技能；README.md 等其他文件跳过
SKILL_SOURCES = {"init.md", "create.md", "apply.md", "fix.md"}


class RenderError(Exception):
    """渲染失败。"""


def load_variables(base_dir: Path) -> dict:
    """读取 Template/vars.json；不存在时返回空字典。"""
    variables_path = base_dir / "Template" / "vars.json"
    if not variables_path.exists():
        return {}
    try:
        return json.loads(variables_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RenderError(f"变量文件不是合法 JSON: {variables_path}: {exc}") from exc


def resolve_variable(path: str, variables: dict) -> str:
    """按点号路径读取变量，例如 skills.apply.name。"""
    current = variables
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise RenderError(f"未定义变量: {{{{@{path}}}}}")
        current = current[part]
    return str(current)


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


def render_content(content: str, base_dir: Path, variables: dict) -> str:
    """
    渲染内容，先替换 {{@path.to.value}}，再替换所有 @Template/xxx.md 占位符

    Args:
        content: 原始内容
        base_dir: 基础目录路径
        variables: 变量字典

    Returns:
        渲染后的内容
    """
    # 先处理变量，允许模板内部继续使用变量
    variable_pattern = r"\{\{@([A-Za-z0-9_.-]+)\}\}"

    def replace_variable(match):
        return resolve_variable(match.group(1), variables)

    content = re.sub(variable_pattern, replace_variable, content)

    # 匹配 @Template/xxx.md 格式的占位符
    pattern = r"@Template/([\w_]+\.md)"

    def replace_placeholder(match):
        """替换占位符为对应文件内容"""
        filename = match.group(1)
        template_path = base_dir / "Template" / filename

        if template_path.exists():
            template_content = read_file_content(template_path)
            # 递归渲染，处理模板中可能包含的其他占位符
            return render_content(template_content, base_dir, variables)
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

    if not source_path.exists() or not source_path.is_dir():
        raise RenderError(f"源目录不存在或不是目录: {source_path}")

    # 先加载变量再清理输出目录，避免变量错误时误删已有产物
    variables = load_variables(source_path)

    # 先全部渲染到内存；任一文件失败则不写入，避免半成品
    rendered_files = []
    for item in source_path.iterdir():
        # 只处理文件，不处理目录
        if not item.is_file():
            continue

        # 跳过隐藏文件和特殊文件
        if item.name.startswith("."):
            continue

        # 只处理技能源文件
        if item.name not in SKILL_SOURCES:
            continue

        print(f"正在处理: {item.name}")

        # 读取文件内容
        content = read_file_content(item)

        # 渲染内容
        rendered_content = render_content(content, source_path, variables)

        # 确定输出路径
        if skill_format:
            # Skill 格式: skills/{name}/SKILL.md
            output_file = output_path / item.stem / "SKILL.md"
        else:
            # 默认格式: dist/{filename}
            output_file = output_path / item.name

        rendered_files.append((output_file, rendered_content, item.name))

    # 全部渲染成功后再清理并写入
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    for output_file, rendered_content, _ in rendered_files:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        write_file_content(output_file, rendered_content)
        print(f"已完成: {output_file}")

    print(f"\n所有文件已渲染到 {output_dir} 目录")


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description="渲染技能源文件：@Template/xxx.md 引入模板，{{@path}} 引入变量"
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

    try:
        render_files(source_dir=args.source, output_dir=output_dir, skill_format=args.skill)
    except RenderError as exc:
        print(f"渲染失败: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
