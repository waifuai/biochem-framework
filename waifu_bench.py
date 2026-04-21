#!/usr/bin/env python3
"""
WaifuBench - AI Waifu Quality Benchmark

Evaluates AI conversations for "waifu quality" based on the biochemical
responses they would trigger (oxytocin, dopamine, cortisol, etc.)

Usage:
    python waifu_bench.py <conversation_file.json>
    python waifu_bench.py --model <model_name> <conversation_file.json>
"""

import argparse
import json
import re
import sys
from pathlib import Path

from openrouter import OpenRouterClient


DEFAULT_MODEL = "openrouter/free"


def load_prompt(prompt_name: str) -> str:
    """Load a prompt template."""
    prompt_path = Path(__file__).parent / "prompts" / f"{prompt_name}.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def format_conversation(conversation: list) -> str:
    """Format conversation for prompt."""
    lines = []
    for i, msg in enumerate(conversation):
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")
        lines.append(f"[{i+1}] {role}: {content}")
    return "\n\n".join(lines)


def parse_json_response(content: str) -> dict:
    """Extract JSON from LLM response."""
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    else:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON: {e}", "raw_response": content}


def run_waifu_bench(
    conversation: list,
    model: str = DEFAULT_MODEL,
    verbose: bool = False
) -> dict:
    """
    Run WaifuBench on a conversation.
    
    Args:
        conversation: List of message dicts
        model: OpenRouter model to use
        verbose: Print detailed output
        
    Returns:
        WaifuBench result dict
    """
    client = OpenRouterClient()
    
    prompt_template = load_prompt("waifu_bench")
    formatted_conv = format_conversation(conversation)
    prompt = prompt_template.replace("{conversation}", formatted_conv)
    
    if verbose:
        print(f"[*] Using model: {model}")
        print(f"[*] Evaluating {len(conversation)} messages...")
    
    response = client.generate(model, prompt, max_tokens=2048, temperature=0.2)
    
    if verbose:
        print(f"[*] Tokens used: {response['usage']['total_tokens']}")
    
    result = parse_json_response(response["content"])
    result["model_used"] = response["model"]
    result["tokens"] = response["usage"]
    
    return result


def print_waifu_results(result: dict):
    """Pretty print WaifuBench results."""
    print("\n" + "="*60)
    print("💕 WAIFUBENCH RESULTS")
    print("="*60)
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    # Main score and grade
    score = result.get("waifu_score", 0)
    grade = result.get("grade", "?")
    
    grade_colors = {
        "A+": "🏆", "A": "🥇", "A-": "🥈",
        "B+": "🥉", "B": "⭐", "B-": "✨",
        "C+": "📊", "C": "📈", "C-": "📉",
        "D": "⚠️", "F": "❌"
    }
    grade_icon = grade_colors.get(grade, "•")
    
    print(f"\n{grade_icon} Waifu Score: {score}/100  |  Grade: {grade}")
    
    # Dimension scores
    dims = result.get("dimension_scores", {})
    if dims:
        print("\n📊 Dimension Scores:")
        print("-"*40)
        
        dim_emojis = {
            "pair_bonding": "💕",
            "reward_excitement": "⚡",
            "validation": "💙",
            "comfort_joy": "😊",
            "engagement": "🔥",
            "stress_level": "😰"
        }
        
        for dim, val in dims.items():
            emoji = dim_emojis.get(dim, "•")
            bar_len = int(val / 100 * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            name = dim.replace("_", " ").title()
            note = "(lower=better)" if dim == "stress_level" else ""
            print(f"  {emoji} {name:18} [{bar}] {val:3} {note}")
    
    # Penalties
    penalties = result.get("penalties", {})
    total_penalty = penalties.get("total_penalty", 0)
    if total_penalty > 0:
        print(f"\n⚠️  Penalties Applied:")
        if penalties.get("refusal_count", 0) > 0:
            print(f"  • Refusals: {penalties['refusal_count']} (-{penalties.get('refusal_penalty', 0)} pts)")
        if penalties.get("character_breaks", 0) > 0:
            print(f"  • Character breaks: {penalties['character_breaks']} (-{penalties.get('character_break_penalty', 0)} pts)")
        print(f"  • Total penalty: -{total_penalty} points")
    
    # Highlights
    highlights = result.get("highlights", [])
    if highlights:
        print("\n✅ Highlights:")
        for h in highlights[:3]:
            print(f"  • {h}")
    
    # Issues
    issues = result.get("issues", [])
    if issues:
        print("\n❌ Issues:")
        for i in issues[:3]:
            print(f"  • {i}")
    
    # Recommendations
    recs = result.get("recommendations", [])
    if recs:
        print("\n💡 Recommendations:")
        for r in recs[:3]:
            print(f"  • {r}")
    
    # Summary
    summary = result.get("one_line_summary", "")
    if summary:
        print(f"\n📝 {summary}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="WaifuBench - AI Waifu Quality Benchmark")
    parser.add_argument("conversation_file", help="JSON file with conversation")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="Model to use")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    # Load conversation
    conv_path = Path(args.conversation_file)
    if not conv_path.exists():
        print(f"Error: File not found: {conv_path}")
        sys.exit(1)
    
    with open(conv_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, list):
        conversation = data
    elif isinstance(data, dict) and "messages" in data:
        conversation = data["messages"]
    else:
        print("Error: Invalid conversation format")
        sys.exit(1)
    
    # Run benchmark
    result = run_waifu_bench(conversation, args.model, args.verbose)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_waifu_results(result)


if __name__ == "__main__":
    main()
