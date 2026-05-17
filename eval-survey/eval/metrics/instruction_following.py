"""维度3: 指令遵循程度评测

评估是否正确遵循 survey_plan.md 的要求。
使用 AB-BA 对称评测，消除位置偏差。
"""

import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, field

from ..utils.llm_client import LLMClient


def _extract_body(tex: str) -> str:
    """剥离 LaTeX 模板代码，只保留正文内容（\\begin{document} 到 \\end{document} 之间）。
    若不含模板结构则原样返回。"""
    m = re.search(r'\\begin\{document\}(.*?)(?:\\end\{document\}|$)', tex, re.DOTALL)
    if m:
        body = m.group(1)
        # 去掉 \maketitle 等无内容命令
        body = re.sub(r'\\(maketitle|tableofcontents|listoffigures)\b\s*', '', body)
        # 去掉 \bibliographystyle / \bibliography 行
        body = re.sub(r'\\bibliography(?:style)?\{[^}]*\}\s*', '', body)
        return body.strip()
    return tex

logger = logging.getLogger(__name__)

INSTRUCTION_FOLLOWING_PROMPT = """你是一位资深学术审稿人。请比较两篇 Related Works 段落，判断哪篇更好地**遵循了任务计划（Survey Plan）的内容要求**。

## 任务要求（Survey Plan）
{plan_content}

## 重要说明
本维度评估计划遵循，并额外评估叙述内容的丰富程度与专业程度（仅限学术内容层面，不看文风偏好）。
- 不要因为文章使用了不同的表达形式（显式 subsection vs 段落内讨论、enumerate 列举 vs 叙述引出）而区别对待
- 只关心：Plan 要求讨论的内容，文章中是否有实质性的对应讨论；以及内容是否充分、专业、具备方法细节
- 关键文献覆盖已由其他模块客观统计，本次不评估

## 文章 A
{tex_a}

## 文章 B
{tex_b}

## 评估维度

1. **主题覆盖** (topic_coverage): Plan 要求讨论的每个研究方向/主题，是否在文中得到了实质性讨论？
   逐一检查 Plan 中列出的各个 Section/Topic，判断文章是否对其有实质内容。无论是通过独立段落还是融入其他讨论中体现，只要有实质内容即算覆盖。
2. **叙事脉络** (narrative_arc): 叙述的逻辑推进是否与 Plan 规定的故事线一致？
   例如 Plan 要求"先 FL 基础 → 通信效率 → 内存效率 → 引出 gap"，文章是否遵循了这个递进顺序？主题出现的先后顺序是否合理？
3. **任务完成** (task_fulfillment): Plan 的 Writing Requirements 中的具体要求是否被实质性满足？
   如 Plan 要求讨论某些方法之间的联系/对比、要求引出某个研究方向的动机等，这些具体指令是否被执行？
4. **内容丰富度** (content_richness): 在不偏离 Plan 的前提下，叙述是否信息密度更高、覆盖面更充分、比较更有层次？
   关注是否提供了充分的方法脉络、关键机制说明、合理的对比维度，而非空泛罗列。
5. **专业程度** (professional_depth): 论述是否体现学术专业性与技术准确性？
   关注术语使用是否准确、方法描述是否专业严谨、是否体现对领域问题与技术路线的深入理解。

请以 JSON 格式输出：
{{
    "relative_scores": {{
        "topic_coverage": -2 到 +2,
        "narrative_arc": -2 到 +2,
        "task_fulfillment": -2 到 +2,
        "content_richness": -2 到 +2,
        "professional_depth": -2 到 +2
    }},
    "reasoning": "逐一说明 Plan 中的各项内容要求在两篇文章中的满足情况，并比较两者的内容丰富度与专业程度，再给出胜负判断。不要基于文风偏好打分。"
}}

relative_scores 含义（每个子维度独立打分）：
  +2 = 文章A 明显优于 B
  +1 = 文章A 略优于 B
   0 = 两者相当
  -1 = 文章B 略优于 A
  -2 = 文章B 明显优于 A"""


DIMENSIONS = [
    "topic_coverage",
    "narrative_arc",
    "task_fulfillment",
    "content_richness",
    "professional_depth",
]
# 最大绝对相对分 = 每子维度满分(2) × 子维度数
_MAX_RAW = 2 * len(DIMENSIONS)  # = 6，归一化目标区间 [-5, +5]


@dataclass
class ABComparisonResult:
    """AB 比较结果（相对分模式）"""
    round_name: str  # "AB" or "BA"
    # relative_scores: 从 A 视角，正=A好，负=B好，每子维度 -2 到 +2
    relative_scores: Dict[str, int] = field(default_factory=dict)
    reasoning: str = ""

    @property
    def total_relative(self) -> int:
        """A 相对于 B 的总原始相对分（本轮，从 A 视角）"""
        return sum(self.relative_scores.values())


@dataclass
class InstructionFollowingEvalResult:
    """指令遵循评测结果"""
    article_a: str
    article_b: str
    round_ab: Optional[ABComparisonResult] = None
    round_ba: Optional[ABComparisonResult] = None

    @property
    def _raw_relative(self) -> float:
        """两轮平均后的原始相对分（A 视角，正=A好）"""
        if not self.round_ab and not self.round_ba:
            return 0.0
        scores = []
        if self.round_ab:
            scores.append(self.round_ab.total_relative)
        if self.round_ba:
            # BA 轮中 relative_scores 的符号已在解析时从 A（即原始 B）视角翻转为 article_a 视角
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
        """兼容字段：根据 relative_score 决定胜者"""
        if self.relative_score > 0:
            return self.article_a
        elif self.relative_score < 0:
            return self.article_b
        return "tie"

    def get_dimension_scores(self) -> Dict[str, float]:
        """各子维度两轮平均相对分（-2 到 +2）"""
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


class InstructionFollowingEvaluator:
    """指令遵循评测器"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def _compare_once(
        self,
        tex_a: str,
        tex_b: str,
        plan_content: str,
        round_name: str,
        invert: bool = False
    ) -> ABComparisonResult:
        """执行一次 AB 比较。
        
        invert=True 时（BA 轮）：将 LLM 返回的相对分取反，
        使其统一为"article_a 视角"（正=article_a 好）。
        """
        prompt = INSTRUCTION_FOLLOWING_PROMPT.format(
            plan_content=plan_content,
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
        plan_path: Path,
        article_a: str = "A",
        article_b: str = "B"
    ) -> InstructionFollowingEvalResult:
        """评估指令遵循程度
        
        使用 AB-BA 对称评测：
        1. 第一轮：A 在前，B 在后
        2. 第二轮：B 在前，A 在后（位置互换）
        3. 综合两轮结果确定胜者
        
        Args:
            tex_path_a: 文章 A 的 tex 文件路径
            tex_path_b: 文章 B 的 tex 文件路径
            plan_path: survey_plan.md 路径
            article_a: 文章 A 的名称
            article_b: 文章 B 的名称
            
        Returns:
            InstructionFollowingEvalResult 评测结果
        """
        tex_a = _extract_body(tex_path_a.read_text(encoding='utf-8'))
        tex_b = _extract_body(tex_path_b.read_text(encoding='utf-8'))
        plan_content = plan_path.read_text(encoding='utf-8')

        logger.info(f"开始指令遵循评测: {article_a} vs {article_b}")

        logger.info("  第一轮: A 在前, B 在后")
        round_ab = self._compare_once(tex_a, tex_b, plan_content, "AB", invert=False)

        logger.info("  第二轮: B 在前, A 在后（符号取反统一为 article_a 视角）")
        round_ba = self._compare_once(tex_b, tex_a, plan_content, "BA", invert=True)

        result = InstructionFollowingEvalResult(
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
    evaluator = InstructionFollowingEvaluator(llm)
    
    result = evaluator.evaluate(
        tex_path_a=sources_dir / "ours" / "related_works.tex",
        tex_path_b=sources_dir / "reas" / "related_works.tex",
        plan_path=sources_dir / "survey_plan.md",
        article_a="ours",
        article_b="reas"
    )
    
    print(f"最终胜者: {result.final_winner}")
    print(f"第一轮: {result.round_ab.winner}")
    print(f"第二轮: {result.round_ba.winner}")
