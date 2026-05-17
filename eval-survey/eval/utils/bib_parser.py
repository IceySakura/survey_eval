"""BibTeX 文件解析器"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class BibEntry:
    """BibTeX 条目"""
    key: str
    entry_type: str  # article, inproceedings, book, etc.
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: str = ""
    venue: str = ""  # journal/booktitle
    arxiv_id: str = ""
    doi: str = ""
    url: str = ""
    abstract: str = ""
    raw_fields: Dict[str, str] = field(default_factory=dict)
    
    @property
    def author_string(self) -> str:
        """返回作者字符串"""
        if len(self.authors) <= 3:
            return ", ".join(self.authors)
        return f"{self.authors[0]} et al."
    
    @property
    def citation_key(self) -> str:
        """返回引用格式"""
        return f"{self.author_string} ({self.year})"


def _clean_latex(text: str) -> str:
    """清理 LaTeX 格式"""
    text = re.sub(r'\{([^{}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+\s*', '', text)
    text = re.sub(r'[${}\\]', '', text)
    text = text.replace('~', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _parse_authors(author_str: str) -> List[str]:
    """解析作者列表"""
    author_str = _clean_latex(author_str)
    authors = re.split(r'\s+and\s+', author_str, flags=re.IGNORECASE)
    result = []
    for author in authors:
        author = author.strip()
        if author:
            if ',' in author:
                parts = author.split(',', 1)
                author = f"{parts[1].strip()} {parts[0].strip()}"
            result.append(author.strip())
    return result


def _extract_arxiv_id(entry_fields: Dict[str, str]) -> str:
    """从各种字段中提取 arXiv ID"""
    eprint = entry_fields.get('eprint', '')
    if eprint:
        match = re.search(r'(\d{4}\.\d{4,5})', eprint)
        if match:
            return match.group(1)
    
    journal = entry_fields.get('journal', '')
    if 'arxiv' in journal.lower():
        match = re.search(r'(\d{4}\.\d{4,5})', journal)
        if match:
            return match.group(1)
    
    url = entry_fields.get('url', '')
    if 'arxiv' in url.lower():
        match = re.search(r'(\d{4}\.\d{4,5})', url)
        if match:
            return match.group(1)
    
    return ""


def parse_bib_file(bib_path: Path) -> List[BibEntry]:
    """解析 BibTeX 文件
    
    Args:
        bib_path: BibTeX 文件路径
        
    Returns:
        BibEntry 列表
    """
    content = bib_path.read_text(encoding='utf-8')
    entries = []
    
    entry_pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,([^@]*?)(?=@|\Z)'
    
    for match in re.finditer(entry_pattern, content, re.DOTALL):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        fields_str = match.group(3)
        
        fields = {}
        field_pattern = r'(\w+)\s*=\s*[{"]((?:[^{}"]|\{[^{}]*\})*)[}"]'
        for field_match in re.finditer(field_pattern, fields_str, re.DOTALL):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            fields[field_name] = field_value
        
        title = _clean_latex(fields.get('title', ''))
        authors = _parse_authors(fields.get('author', ''))
        year = fields.get('year', '')
        venue = fields.get('journal', '') or fields.get('booktitle', '')
        venue = _clean_latex(venue)
        arxiv_id = _extract_arxiv_id(fields)
        doi = fields.get('doi', '')
        url = fields.get('url', '')
        abstract = _clean_latex(fields.get('abstract', ''))
        
        entry = BibEntry(
            key=key,
            entry_type=entry_type,
            title=title,
            authors=authors,
            year=year,
            venue=venue,
            arxiv_id=arxiv_id,
            doi=doi,
            url=url,
            abstract=abstract,
            raw_fields=fields
        )
        entries.append(entry)
    
    return entries


def extract_citations_from_tex(tex_path: Path) -> Dict[str, List[str]]:
    """从 tex 文件中提取引用及其上下文
    
    Args:
        tex_path: tex 文件路径
        
    Returns:
        {citation_key: [surrounding_contexts]} 字典
    """
    content = tex_path.read_text(encoding='utf-8')
    
    cite_pattern = r'\\cite[tp]?\{([^}]+)\}'
    citations = {}
    
    for match in re.finditer(cite_pattern, content):
        keys = [k.strip() for k in match.group(1).split(',')]
        start = max(0, match.start() - 300)
        end = min(len(content), match.end() + 100)
        context = content[start:end]
        context = re.sub(r'\s+', ' ', context).strip()
        
        for key in keys:
            if key not in citations:
                citations[key] = []
            citations[key].append(context)
    
    return citations


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        bib_path = Path(sys.argv[1])
        entries = parse_bib_file(bib_path)
        print(f"解析到 {len(entries)} 条引用:")
        for entry in entries[:5]:
            print(f"  - {entry.key}: {entry.title[:50]}... ({entry.year})")
