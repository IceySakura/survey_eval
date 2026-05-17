"""文件系统工具"""

import shutil
import difflib
from pathlib import Path
from typing import List, Callable

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
BLOCKED_EXTENSIONS = {".exe", ".dll", ".so", ".dylib", ".bin"}


def create_file_tools(workspace: str) -> List[Callable]:
    """创建文件系统工具函数列表"""

    workspace_root = Path(workspace).resolve()
    workspace_root.mkdir(parents=True, exist_ok=True)

    def validate_path(path: str) -> Path:
        if not path:
            return workspace_root
        full_path = (workspace_root / path).resolve()
        if not str(full_path).startswith(str(workspace_root)):
            raise ValueError(f"路径不在工作空间内: {path}")
        return full_path

    def read_file(path: str) -> str:
        try:
            file_path = validate_path(path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {path}")
            if not file_path.is_file():
                raise ValueError(f"路径不是文件: {path}")
            if file_path.stat().st_size > MAX_FILE_SIZE:
                raise ValueError(f"文件过大: {path}")
            content = file_path.read_text(encoding="utf-8")
            logger.info(f"读取文件: {path}, 大小: {len(content)} 字符")
            return f"文件内容:\n{content}"
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            raise

    def write_file(path: str, content: str) -> str:
        try:
            file_path = validate_path(path)
            if file_path.suffix.lower() in BLOCKED_EXTENSIONS:
                raise ValueError(f"不允许的文件类型: {file_path.suffix}")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"写入文件: {path}, 大小: {len(content)} 字符")
            return f"文件已写入: {path}"
        except Exception as e:
            logger.error(f"写入文件失败: {e}")
            raise

    def list_directory(path: str) -> str:
        try:
            dir_path = validate_path(path)
            if not dir_path.exists():
                raise FileNotFoundError(f"目录不存在: {path}")
            if not dir_path.is_dir():
                raise ValueError(f"路径不是目录: {path}")
            items = []
            for item in sorted(dir_path.iterdir()):
                item_type = "目录" if item.is_dir() else "文件"
                size = f", 大小: {item.stat().st_size} 字节" if item.is_file() else ""
                items.append(f"- {item.name} ({item_type}{size})")
            result = f"目录内容 ({path or '根目录'}):\n" + "\n".join(items)
            logger.info(f"列出目录: {path}, 项目数: {len(items)}")
            return result
        except Exception as e:
            logger.error(f"列出目录失败: {e}")
            raise

    def create_directory(path: str) -> str:
        try:
            dir_path = validate_path(path)
            if dir_path.exists():
                if dir_path.is_dir():
                    logger.info(f"目录已存在，跳过创建: {path}")
                    return f"目录已存在（可继续使用）: {path}"
                raise ValueError(f"路径已存在且不是目录: {path}")
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建目录: {path}")
            return f"目录已创建: {path}"
        except Exception as e:
            logger.error(f"创建目录失败: {e}")
            raise

    def delete_file(path: str) -> str:
        try:
            file_path = validate_path(path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {path}")
            if not file_path.is_file():
                raise ValueError(f"路径不是文件: {path}")
            file_path.unlink()
            logger.info(f"删除文件: {path}")
            return f"文件已删除: {path}"
        except Exception as e:
            logger.error(f"删除文件失败: {e}")
            raise

    def edit_file(
        path: str, old_string: str, new_string: str, replace_all: bool = False
    ) -> str:
        try:
            file_path = validate_path(path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {path}")
            if not file_path.is_file():
                raise ValueError(f"路径不是文件: {path}")
            original_content = file_path.read_text(encoding="utf-8")
            if old_string not in original_content:
                error_msg = f"在文件中未找到要替换的文本。\n"
                error_msg += f"要查找的文本 ({len(old_string)} 字符):\n"
                error_msg += f"```\n{old_string[:500]}{'...' if len(old_string) > 500 else ''}\n```"
                raise ValueError(error_msg)
            if replace_all:
                new_content = original_content.replace(old_string, new_string)
                replacement_count = original_content.count(old_string)
            else:
                new_content = original_content.replace(old_string, new_string, 1)
                replacement_count = 1
            original_lines = original_content.splitlines(keepends=True)
            new_lines = new_content.splitlines(keepends=True)
            diff = difflib.unified_diff(
                original_lines,
                new_lines,
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
                lineterm="",
            )
            diff_text = "".join(diff)
            file_path.write_text(new_content, encoding="utf-8")
            logger.info(f"编辑文件: {path}, 替换 {replacement_count} 处")
            result = f"文件已编辑: {path}\n"
            result += f"替换了 {replacement_count} 处匹配\n\n"
            if diff_text:
                result += f"Diff:\n```diff\n{diff_text}\n```"
            return result
        except Exception as e:
            logger.error(f"编辑文件失败: {e}")
            raise

    def move_file(source: str, destination: str) -> str:
        try:
            source_path = validate_path(source)
            dest_path = validate_path(destination)
            if not source_path.exists():
                raise FileNotFoundError(f"源路径不存在: {source}")
            if dest_path.exists():
                raise ValueError(f"目标路径已存在: {destination}")
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_path))
            item_type = "目录" if dest_path.is_dir() else "文件"
            logger.info(f"移动{item_type}: {source} -> {destination}")
            return f"{item_type}已移动: {source} -> {destination}"
        except Exception as e:
            logger.error(f"移动文件失败: {e}")
            raise

    return [
        read_file,
        write_file,
        list_directory,
        create_directory,
        delete_file,
        edit_file,
        move_file,
    ]
