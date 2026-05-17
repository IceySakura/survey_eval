"""论文下载器 - 从 arXiv 下载 PDF 并提取文本

复用自 enrich_topics_analysis.py 的逻辑
"""

import re
import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple
import requests

logger = logging.getLogger(__name__)

HTTP_PROXY = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
HTTPS_PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
PROXIES = {}
if HTTP_PROXY:
    PROXIES['http'] = HTTP_PROXY
if HTTPS_PROXY:
    PROXIES['https'] = HTTPS_PROXY


class PaperFetcher:
    """论文下载器"""
    
    def __init__(self, cache_dir: Optional[Path] = None, max_chars: int = 50000):
        """初始化论文下载器
        
        Args:
            cache_dir: 缓存目录路径
            max_chars: PDF 提取的最大字符数
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "cache"
        
        self.cache_dir = cache_dir
        self.pdf_cache_dir = cache_dir / "pdf"
        self.text_cache_dir = cache_dir / "text"
        self.max_chars = max_chars
        
        self._ensure_cache_dirs()
    
    def _ensure_cache_dirs(self):
        """确保缓存目录存在"""
        self.pdf_cache_dir.mkdir(parents=True, exist_ok=True)
        self.text_cache_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_arxiv_pdf(self, arxiv_id: str) -> Tuple[Optional[str], Optional[int]]:
        """从 arXiv 下载 PDF 并提取文本
        
        Args:
            arxiv_id: arXiv ID (如 "2403.03165" 或 "2403.03165v1")
        
        Returns:
            (文本内容, HTTP状态码): 成功时 (text, None)，HTTP 失败时 (None, status_code)，其他失败 (None, None)
        """
        clean_id = re.sub(r'v\d+$', '', arxiv_id)
        cache_filename = clean_id.replace('/', '_')
        pdf_cache_path = self.pdf_cache_dir / f"{cache_filename}.pdf"
        text_cache_path = self.text_cache_dir / f"{cache_filename}.txt"
        
        if text_cache_path.exists():
            logger.info(f"  [缓存] 使用已有文本: {clean_id}")
            text = text_cache_path.read_text(encoding='utf-8')
            if len(text) > self.max_chars:
                text = text[:self.max_chars] + "\n...[truncated]"
            return (text, None)
        
        if pdf_cache_path.exists():
            logger.info(f"  [缓存] 使用已有 PDF: {clean_id}")
        else:
            url = f"https://arxiv.org/pdf/{clean_id}.pdf"
            
            try:
                logger.info(f"  [PDF] 正在下载: {clean_id}...")
                response = requests.get(
                    url, 
                    timeout=300, 
                    stream=True, 
                    proxies=PROXIES if PROXIES else None
                )
                
                if response.status_code != 200:
                    logger.info(f"  [PDF] 下载失败 (HTTP {response.status_code})")
                    return (None, response.status_code)
                
                with open(pdf_cache_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                logger.info(f"  [PDF] 下载完成: {pdf_cache_path.name}")
                
            except requests.RequestException as e:
                logger.warning(f"  [PDF] 网络错误: {e}")
                if pdf_cache_path.exists():
                    pdf_cache_path.unlink()
                return (None, None)
        
        logger.info(f"  [PDF] 正在转换文本...")
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', str(pdf_cache_path), '-'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.warning(f"  [PDF] pdftotext 失败: {result.stderr[:100]}")
                return (None, None)
            
            text = result.stdout
            
        except FileNotFoundError:
            logger.warning("  [PDF] pdftotext 未安装，请运行: sudo apt install poppler-utils")
            return (None, None)
        except subprocess.TimeoutExpired:
            logger.warning("  [PDF] pdftotext 超时")
            return (None, None)
        
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        text = text.strip()
        
        text_cache_path.write_text(text, encoding='utf-8')
        logger.info(f"  [PDF] 文本已缓存: {text_cache_path.name}")
        
        if len(text) > self.max_chars:
            text = text[:self.max_chars] + "\n...[truncated]"
        
        return (text, None)
    
    def get_paper_content(self, arxiv_id: Optional[str] = None, doi: Optional[str] = None) -> Tuple[Optional[str], Optional[int]]:
        """获取论文内容
        
        Args:
            arxiv_id: arXiv ID
            doi: DOI
            
        Returns:
            (文本内容, HTTP状态码): 成功 (text, None)，HTTP 失败 (None, status_code)，其他 (None, None)
        """
        if arxiv_id:
            return self.fetch_arxiv_pdf(arxiv_id)
        
        if doi:
            logger.warning(f"暂不支持通过 DOI 下载论文: {doi}")
            return (None, None)
        
        return (None, None)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetcher = PaperFetcher()
    text, status = fetcher.fetch_arxiv_pdf("2403.03165")
    if text:
        print(f"获取到 {len(text)} 字符")
        print(text[:500])
