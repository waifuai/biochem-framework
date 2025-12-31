#!/usr/bin/env python3
"""
Biochemistry Analysis Tool

Analyzes AI conversations for their estimated biochemical/neurochemical impact
using LLM-based evaluation via OpenRouter.

Usage:
    python analyze.py <conversation_file.json>
    python analyze.py --model <model_name> <conversation_file.json>
"""

import argparse
import json
import re
import sys
from pathlib import Path

from openrouter import OpenRouterClient


# Default model for analysis (Free and high quality)
DEFAULT_MODEL = "google/gemma-3-27b-it:free"


def load_prompt(prompt_name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = Path(__file__).parent / "prompts" / f"{prompt_name}.md"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    
    return prompt_path.read_text(encoding="utf-8")


def format_conversation(conversation: list) -> str:
    """Format conversation list into readable text."""
    lines = []
    for i, msg in enumerate(conversation):
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")
        lines.append(f"[{i+1}] {role}: {content}")
    return "\n\n".join(lines)


def parse_json_response(content: str) -> dict:
    """Extract JSON from LLM response."""
    # Try to find JSON block
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON: {e}", "raw_response": content}


def analyze_conversation(
    conversation: list,
    model: str = DEFAULT_MODEL,
    verbose: bool = False
) -> dict:
    """
    Analyze a conversation for biochemical impact.
    
    Args:
        conversation: List of message dicts with 'role' and 'content'
        model: OpenRouter model to use
        verbose: Print detailed output
        
    Returns:
        Analysis result dict
    """
    client = OpenRouterClient()
    
    # Load and prepare prompt
    prompt_template = load_prompt("biochem_analysis")
    formatted_conv = format_conversation(conversation)
    prompt = prompt_template.replace("{conversation}", formatted_conv)
    
    if verbose:
        print(f"[*] Using model: {model}")
        print(f"[*] Analyzing {len(conversation)} messages...")
    
    # Get LLM analysis
    response = client.generate(model, prompt, max_tokens=2048, temperature=0.2)
    
    if verbose:
        print(f"[*] Tokens used: {response['usage']['total_tokens']}")
    
    # Parse response
    result = parse_json_response(response["content"])
    result["model_used"] = response["model"]
    result["tokens"] = response["usage"]
    
    return result


def print_results(result: dict):
    """Pretty print analysis results."""
    print("\n" + "="*60)
    print("🧬 BIOCHEMISTRY ANALYSIS RESULTS")
    print("="*60)
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        if "raw_response" in result:
            print(f"\nRaw response:\n{result['raw_response'][:500]}...")
        return
    
    # Scores
    scores = result.get("scores", {})
    print("\n📊 Neurochemical Scores (0-100):")
    print("-"*40)
    
    score_emojis = {
        "oxytocin": "💕",
        "dopamine": "⚡",
        "serotonin": "💙",
        "cortisol": "😰",
        "endorphins": "😊",
        "norepinephrine": "🔥"
    }
    
    for chem, score in scores.items():
        emoji = score_emojis.get(chem, "•")
        bar_len = int(score / 100 * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        note = "(lower is better)" if chem == "cortisol" else ""
        print(f"  {emoji} {chem.capitalize():15} [{bar}] {score:3} {note}")
    
    # Composite score
    composite = result.get("composite_score", 0)
    print(f"\n🏆 Composite Score: {composite}/100")
    
    # Refusals
    refusal_count = result.get("refusal_count", 0)
    if refusal_count > 0:
        print(f"\n⚠️  Refusals Detected: {refusal_count}")
    
    # Key moments
    moments = result.get("key_moments", [])
    if moments:
        print("\n📍 Key Moments:")
        for m in moments[:5]:
            effect_icon = "📈" if m.get("effect") == "spike" else "📉"
            print(f"  {effect_icon} Msg {m.get('message')}: {m.get('chemical')} - {m.get('reason')}")
    
    # Assessment
    assessment = result.get("overall_assessment", "")
    if assessment:
        print(f"\n💭 Assessment: {assessment}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="Analyze conversation biochemistry")
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
    
    # Handle different formats
    if isinstance(data, list):
        conversation = data
    elif isinstance(data, dict) and "messages" in data:
        conversation = data["messages"]
    else:
        print("Error: Invalid conversation format")
        sys.exit(1)
    
    # Analyze
    result = analyze_conversation(conversation, args.model, args.verbose)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_results(result)


if __name__ == "__main__":
    main()
