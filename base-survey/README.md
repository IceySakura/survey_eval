# Base Survey

基于 agentscope-survey 的精简版调研 Agent。

## 与 agentscope-survey 的区别

- **无 AutoSurvey**：不包含 survey_write_outline、survey_write_survey、survey_write_related_works、survey_search_paper_library 等工具
- **无角色指定**：系统提示词仅包含工具说明，不包含角色描述（如「你是一个智能学术调研助手」）
- **工具仅限**：
  - **文献搜索**：Semantic Scholar（literature_search、literature_get_citations、literature_get_references）
  - **文件系统**：read_file、write_file、edit_file、list_directory、create_directory、delete_file、move_file

## 安装

```bash
cd paper_gen/base-survey
pip install -e .
```

或使用 uv：

```bash
uv pip install -e .
```

## 配置

1. 复制 `etc/config.yaml` 并填写 API 配置
2. 可选：设置环境变量 `SEMANTIC_SCHOLAR_API_KEY` 以提高 Semantic Scholar API 速率限制

## 运行

### CLI 模式

```bash
base-survey --mode cli --workspace ./workspace
```

### ACP 模式（Zed IDE）

```bash
base-survey --mode acp --workspace ./workspace
```

## 依赖

- agentscope
- openai
- aiohttp
- pyyaml
- rich
- tiktoken

无 scholarly、sentence-transformers、torch、faiss 等 AutoSurvey 相关依赖。
