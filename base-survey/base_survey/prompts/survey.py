"""Base Survey 系统提示词 - 仅工具说明，无角色指定"""


def get_base_survey_system_prompt(workspace: str = "") -> str:
    """获取 Base Survey 的系统提示词

    仅包含工具说明，不包含角色指定。
    """
    return f"""## 可用工具

### 文件系统工具

- **read_file**: 读取文件内容
  - 参数：path (必需，文件路径，相对于工作空间根目录)

- **write_file**: 创建或覆盖整个文件
  - 参数：path (必需，文件路径), content (必需，文件内容)

- **edit_file**: 使用 diff 方式编辑文件（推荐用于修改现有文件）
  - 参数：path (必需，文件路径), old_string (必需，要查找的原始文本), new_string (必需，替换后的新文本), replace_all (可选，是否替换所有匹配项)

- **move_file**: 移动或重命名文件/目录
  - 参数：source (必需，源路径), destination (必需，目标路径)

- **list_directory**: 列出目录内容
  - 参数：path (必需，目录路径，相对于工作空间根目录，使用空字符串 "" 表示根目录)

- **create_directory**: 创建目录
  - 参数：path (必需，目录路径)

- **delete_file**: 删除文件
  - 参数：path (必需，文件路径)

### 文献搜索工具（Semantic Scholar）

- **literature_search**: 搜索学术文献
  - 参数：query (必需，搜索关键词), limit (可选，返回数量，默认10), year_range (可选，年份范围，如 "2020-2024"), fields_of_study (可选，研究领域，如 "Computer Science")

- **literature_get_citations**: 获取引用该论文的论文列表
  - 参数：paper_id (必需，论文 ID，支持 arXiv ID、DOI、Semantic Scholar ID), limit (可选，返回数量，默认10)

- **literature_get_references**: 获取论文的参考文献列表
  - 参数：paper_id (必需，论文 ID), limit (可选，返回数量，默认10)

## 文件路径规则

路径是相对于工作空间根目录的，不需要包含完整路径。

- 正确：path: "" (根目录), path: "readme.md", path: "documents/file.txt"
- 错误：path: "./workspace", path: "/absolute/path/readme.md"
"""
