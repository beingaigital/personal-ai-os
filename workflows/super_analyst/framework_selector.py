from __future__ import annotations

from typing import List, Dict, Tuple
import re
from pathlib import Path
import json


DEFAULT_FRAMEWORKS: List[Dict] = [
    {
        "id": "first_principles",
        "name": "First Principles Thinking",
        "prompt_template": "first_principles.md",
        "keywords": ["root cause", "fundamental", "assumption", "principle", "from scratch", "break down"],
        "problem_types": ["innovation", "architecture", "complex decision"],
        "complexity": "high",
        "expected_time": "medium",
        "description": "Break down to fundamentals and rebuild solutions.",
    },
    {
        "id": "five_whys",
        "name": "5 Whys",
        "prompt_template": "five_whys.md",
        "keywords": ["why", "incident", "bug", "failure", "postmortem", "root cause"],
        "problem_types": ["diagnosis", "quality", "ops"],
        "complexity": "low",
        "expected_time": "short",
        "description": "Iteratively ask 'why' to find root causes.",
    },
    {
        "id": "swot",
        "name": "SWOT Analysis",
        "prompt_template": "swot.md",
        "keywords": ["strength", "weakness", "opportunity", "threat", "strategy", "position"],
        "problem_types": ["business", "product", "market"],
        "complexity": "medium",
        "expected_time": "medium",
        "description": "Assess internal and external factors.",
    },
    {
        "id": "five_forces",
        "name": "Porter's Five Forces",
        "prompt_template": "five_forces.md",
        "keywords": ["industry", "competition", "supplier", "buyer", "substitute", "entrant"],
        "problem_types": ["industry analysis", "investment"],
        "complexity": "medium",
        "expected_time": "medium",
        "description": "Evaluate competitive intensity in an industry.",
    },
    {
        "id": "cost_benefit",
        "name": "Cost-Benefit Analysis",
        "prompt_template": "cost_benefit.md",
        "keywords": ["cost", "benefit", "roi", "trade-off", "valuation", "budget"],
        "problem_types": ["investment", "project"],
        "complexity": "medium",
        "expected_time": "short",
        "description": "Weigh costs and benefits with assumptions.",
    },
    {
        "id": "design_thinking",
        "name": "Design Thinking",
        "prompt_template": "design_thinking.md",
        "keywords": ["user", "empathize", "prototype", "ux", "journey", "test"],
        "problem_types": ["product", "experience", "service"],
        "complexity": "medium",
        "expected_time": "medium",
        "description": "User-centered iterative innovation process.",
    },
    {
        "id": "systems_thinking",
        "name": "Systems Thinking",
        "prompt_template": "systems_thinking.md",
        "keywords": ["system", "feedback loop", "stock and flow", "leverage", "ripple"],
        "problem_types": ["complex system", "policy"],
        "complexity": "high",
        "expected_time": "long",
        "description": "Analyze structures, dynamics and feedbacks.",
    },
    {
        "id": "socratic",
        "name": "Socratic Method",
        "prompt_template": "socratic.md",
        "keywords": ["assumption", "question", "clarify", "counterexample", "dialectic"],
        "problem_types": ["ethics", "concept", "ambiguity"],
        "complexity": "low",
        "expected_time": "short",
        "description": "Probe assumptions via targeted questions.",
    },
    {
        "id": "pareto",
        "name": "Pareto Analysis",
        "prompt_template": "pareto.md",
        "keywords": ["80/20", "pareto", "vital few", "long tail", "prioritize"],
        "problem_types": ["prioritization", "optimization"],
        "complexity": "low",
        "expected_time": "short",
        "description": "Focus on the vital few causes for outcomes.",
    },
    {
        "id": "hypothesis_driven",
        "name": "Hypothesis-Driven Analysis",
        "prompt_template": "hypothesis_driven.md",
        "keywords": ["hypothesis", "test", "evidence", "falsify", "experiment"],
        "problem_types": ["research", "strategy", "product"],
        "complexity": "medium",
        "expected_time": "medium",
        "description": "Formulate and test hypotheses quickly.",
    },
    {
        "id": "scenario_planning",
        "name": "Scenario Planning",
        "prompt_template": "scenario_planning.md",
        "keywords": ["scenario", "uncertainty", "future", "risk", "contingency"],
        "problem_types": ["strategy", "risk"],
        "complexity": "medium",
        "expected_time": "medium",
        "description": "Explore multiple plausible futures.",
    },
    {
        "id": "mece",
        "name": "MECE Principle",
        "prompt_template": "mece.md",
        "keywords": ["mutually exclusive", "collectively exhaustive", "structure", "taxonomy"],
        "problem_types": ["decomposition", "analysis structure"],
        "complexity": "low",
        "expected_time": "short",
        "description": "Create clear, non-overlapping analytical structures.",
    },
]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def _load_external_frameworks() -> List[Dict]:
    """
    Try to load frameworks from config/frameworks.json.
    If present but missing 'prompt_template', attempt to infer it as '<id>.md'.
    If the prompts file does not exist, fallback to defaults.
    """
    root = Path(__file__).resolve().parents[2]
    cfg_path = root / "config" / "frameworks.json"
    prompts_dir = Path(__file__).resolve().parent / "prompts"
    if not cfg_path.exists():
        return []
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        items = data.get("frameworks", [])
        enriched: List[Dict] = []
        for fw in items:
            fw_copy = dict(fw)
            if "prompt_template" not in fw_copy:
                guess = f"{fw_copy.get('id', '')}.md"
                # Use guess only if file exists; otherwise skip this fw to avoid runtime errors
                if (prompts_dir / guess).exists():
                    fw_copy["prompt_template"] = guess
                else:
                    # try some simple aliases
                    alias_map = {
                        "porter_five_forces": "five_forces.md",
                    }
                    alias_guess = alias_map.get(fw_copy.get("id", ""), "")
                    if alias_guess and (prompts_dir / alias_guess).exists():
                        fw_copy["prompt_template"] = alias_guess
                    else:
                        continue
            enriched.append(fw_copy)
        return enriched
    except Exception:
        return []


FRAMEWORKS: List[Dict] = _load_external_frameworks() or DEFAULT_FRAMEWORKS


def analyze_text(question: str) -> List[Tuple[Dict, int, List[str]]]:
    tokens = set(_tokenize(question))
    scored: List[Tuple[Dict, int, List[str]]] = []
    for fw in FRAMEWORKS:
        matched = [kw for kw in fw["keywords"] if any(k in tokens or k.replace(" ", "") in "".join(tokens) for k in [kw.lower()])]
        score = len(matched)
        scored.append((fw, score, matched))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def recommend_frameworks(question: str, top_n: int = 3) -> List[Dict]:
    ranked = analyze_text(question)
    recs = []
    for fw, score, matched in ranked[:top_n]:
        recs.append({
            "id": fw["id"],
            "name": fw["name"],
            "prompt_template": fw["prompt_template"],
            "score": score,
            "matched_keywords": matched,
            "description": fw["description"],
        })
    return recs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Framework selector")
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args()
    out = recommend_frameworks(args.question, args.top)
    print(json.dumps(out, ensure_ascii=False, indent=2))


