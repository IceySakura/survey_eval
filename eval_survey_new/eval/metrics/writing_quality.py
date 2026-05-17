"""维度4: 写作质量评测

评估学术写作质量。
使用 AB-BA 对称评测，消除位置偏差。
参考顶会 Related Works 写作规范设计评测标准。
"""

import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from ..utils.llm_client import LLMClient


def _extract_body(tex: str) -> str:
    """剥离 LaTeX 模板代码，只保留正文内容（\\begin{document} 到 \\end{document} 之间）。
    若不含模板结构则原样返回。"""
    m = re.search(r'\\begin\{document\}(.*?)(?:\\end\{document\}|$)', tex, re.DOTALL)
    if m:
        body = m.group(1)
        body = re.sub(r'\\(maketitle|tableofcontents|listoffigures)\b\s*', '', body)
        body = re.sub(r'\\bibliography(?:style)?\{[^}]*\}\s*', '', body)
        return body.strip()
    return tex

logger = logging.getLogger(__name__)

WRITING_QUALITY_PROMPT = """你是一位顶级学术会议（ICML/NeurIPS/ICLR）的资深审稿人。请比较两篇 Related Works 段落的**写作质量**。

## 评价定位
这些 Related Works 是研究论文的一个章节，不是独立的综述文章。
在顶级会议论文中，最好的 Related Works 用最少的篇幅传递最多的信息，每一句话都为论文的贡献服务。
以下是本次评价的核心标准：
- **高密度优于低密度**：同等信息量，用更少篇幅完成的写作更好
- **自然涌现优于显式声明**：研究动机在叙述中有机浮现，优于用独立段落或标签显式声明
- **冗余是负面因素**：重复的背景铺垫、显式的格式标签（如 \\textbf{{Key Limitation:}}）、枚举式 Gap 列表如果只是重复前文已表达的信息，应被视为密度损失
- 本维度不评估"是否覆盖了 Plan 要求的内容"——那是其他维度的职责

## 文章 A
{tex_a}

## 文章 B
{tex_b}

## 评估维度

1. **信息密度** (density): 每句话是否都承载有意义的技术信息？
   - 同等内容量下，用更少篇幅完成 = 更高分
   - 冗余的过渡句、重复的背景铺垫、为排版而设的格式标签是密度损失
   - 一个段落中有意义地讨论多篇文献并建立联系，优于每篇文献用独立段落泛泛介绍

2. **技术深度** (depth): 对引用工作的讨论是否深入到方法机制、理论假设、收敛性质等层面？
   - 是否超越"X 提出了 Y"的表面描述，触及方法的核心思想和技术细节？
   - 是否展示了对所引用工作的真正理解？

3. **批判性综合** (synthesis): 是否在讨论中自然地对比不同方法、指出联系和权衡？
   - 是否将多个相关工作放在一起分析其异同？
   - 是否识别出方法之间的理论联系或实践权衡？
   - 在叙述流中自然指出局限，优于孤立的"Key Limitation"标签

4. **动机涌现** (motivation): 读完之后，读者是否自然理解为什么需要本文的工作？
   - 评价的是动机**涌现的自然程度**：在叙述中有机地让读者感受到 gap，优于在文末用独立段落显式声明 gap
   - 如果文末的 Gap 段落只是重复前文叙述中已经表达清楚的信息，应被视为冗余而非加分项

请以 JSON 格式输出：
{{
    "relative_scores": {{
        "density": -2 到 +2,
        "depth": -2 到 +2,
        "synthesis": -2 到 +2,
        "motivation": -2 到 +2
    }},
    "reasoning": "对每篇文章的信息密度、技术深度、综合分析和动机构建分别评价，再给出胜负判断。关注内容实质而非排版格式。"
}}

relative_scores 含义（每个子维度独立打分）：
  +2 = 文章A 明显优于 B
  +1 = 文章A 略优于 B
   0 = 两者相当
  -1 = 文章B 略优于 A
  -2 = 文章B 明显优于 A"""


DIMENSIONS = ["density", "depth", "synthesis", "motivation"]
_MAX_RAW = 2 * len(DIMENSIONS)  # = 8，归一化目标区间 [-5, +5]


@dataclass
class ABComparisonResult:
    """AB 比较结果（相对分模式）"""
    round_name: str
    relative_scores: Dict[str, int] = field(default_factory=dict)
    reasoning: str = ""

    @property
    def total_relative(self) -> int:
        return sum(self.relative_scores.values())


@dataclass
class WritingQualityEvalResult:
    """写作质量评测结果"""
    article_a: str
    article_b: str
    round_ab: Optional[ABComparisonResult] = None
    round_ba: Optional[ABComparisonResult] = None

    @property
    def _raw_relative(self) -> float:
        """两轮平均原始相对分（article_a 视角，正=a 好）"""
        if not self.round_ab and not self.round_ba:
            return 0.0
        scores = []
        if self.round_ab:
            scores.append(self.round_ab.total_relative)
        if self.round_ba:
            scores.append(self.round_ba.total_relative)
        return sum(scores) / len(scores)

    @property
    def relative_score(self) -> float:
        """归一化到 [-5, +5]，正=article_a 好，负=article_b 好"""
        if _MAX_RAW == 0:
            return 0.0
        return round(self._raw_relative / _MAX_RAW * 5, 2)

    @property
    def final_winner(self) -> str:
        if self.relative_score > 0:
            return self.article_a
        elif self.relative_score < 0:
            return self.article_b
        return "tie"

    def get_dimension_scores(self) -> Dict[str, float]:
        """各子维度两轮平均相对分（-2 到 +2，article_a 视角）"""
        result = {}
        for dim in DIMENSIONS:
            vals = []
            if self.round_ab:
                vals.append(self.round_ab.relative_scores.get(dim, 0))
            if self.round_ba:
                vals.append(self.round_ba.relative_scores.get(dim, 0))
            result[dim] = round(sum(vals) / len(vals), 2) if vals else 0.0
        return result

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "article_a": self.article_a,
            "article_b": self.article_b,
            "relative_score": self.relative_score,
            "final_winner": self.final_winner,
            "dimension_scores": self.get_dimension_scores(),
            "round_ab": {
                "relative_scores": self.round_ab.relative_scores if self.round_ab else {},
                "reasoning": self.round_ab.reasoning if self.round_ab else ""
            },
            "round_ba": {
                "relative_scores": self.round_ba.relative_scores if self.round_ba else {},
                "reasoning": self.round_ba.reasoning if self.round_ba else ""
            }
        }


class WritingQualityEvaluator:
    """写作质量评测器"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def _compare_once(
        self,
        tex_a: str,
        tex_b: str,
        round_name: str,
        invert: bool = False
    ) -> ABComparisonResult:
        """执行一次 AB 比较。
        
        invert=True 时（BA 轮）：将 LLM 返回的相对分取反，
        使其统一为"article_a 视角"（正=article_a 好）。
        """
        prompt = WRITING_QUALITY_PROMPT.format(
            tex_a=tex_a[:8000],
            tex_b=tex_b[:8000]
        )

        result = self.llm.chat_json(prompt)

        if result is None:
            logger.warning(f"比较失败: {round_name}")
            return ABComparisonResult(
                round_name=round_name,
                reasoning="LLM 评估失败"
            )

        raw_rel = result.get("relative_scores", {})
        relative_scores = {}
        for dim in DIMENSIONS:
            val = int(raw_rel.get(dim, 0))
            val = max(-2, min(2, val))
            relative_scores[dim] = -val if invert else val

        return ABComparisonResult(
            round_name=round_name,
            relative_scores=relative_scores,
            reasoning=result.get("reasoning", "")
        )
    
    def evaluate(
        self,
        tex_path_a: Path,
        tex_path_b: Path,
        article_a: str = "A",
        article_b: str = "B"
    ) -> WritingQualityEvalResult:
        """评估写作质量
        
        使用 AB-BA 对称评测：
        1. 第一轮：A 在前，B 在后
        2. 第二轮：B 在前，A 在后（位置互换）
        3. 综合两轮结果确定胜者
        
        Args:
            tex_path_a: 文章 A 的 tex 文件路径
            tex_path_b: 文章 B 的 tex 文件路径
            article_a: 文章 A 的名称
            article_b: 文章 B 的名称
            
        Returns:
            WritingQualityEvalResult 评测结果
        """
        tex_a = _extract_body(tex_path_a.read_text(encoding='utf-8'))
        tex_b = _extract_body(tex_path_b.read_text(encoding='utf-8'))

        logger.info(f"开始写作质量评测: {article_a} vs {article_b}")

        logger.info("  第一轮: A 在前, B 在后")
        round_ab = self._compare_once(tex_a, tex_b, "AB", invert=False)

        logger.info("  第二轮: B 在前, A 在后（符号取反统一为 article_a 视角）")
        round_ba = self._compare_once(tex_b, tex_a, "BA", invert=True)

        result = WritingQualityEvalResult(
            article_a=article_a,
            article_b=article_b,
            round_ab=round_ab,
            round_ba=round_ba
        )

        logger.info(f"  相对分: {result.relative_score:+.2f} / 5.0"
                    f"  胜者: {result.final_winner}")
        
        return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    eval_dir = Path(__file__).parent.parent
    sources_dir = eval_dir.parent / "sources"
    
    llm = LLMClient()
    evaluator = WritingQualityEvaluator(llm)
    
    result = evaluator.evaluate(
        tex_path_a=sources_dir / "ours" / "related_works.tex",
        tex_path_b=sources_dir / "reas" / "related_works.tex",
        article_a="ours",
        article_b="reas"
    )
    
    print(f"最终胜者: {result.final_winner}")
    print(f"各维度分析: {result.get_dimension_analysis()}")
