# 🧬 Biochem Framework

**Benchmark AI conversations by their estimated biochemical impact using LLM analysis.**

## Overview

Traditional AI benchmarks measure coherence and accuracy. **Biochem Framework** measures the *physiological impact* - what neurochemicals would be released when interacting with an AI.

- **Oxytocin** (bonding) - trust, intimacy, emotional safety
- **Dopamine** (reward) - excitement, anticipation, flirtation
- **Serotonin** (validation) - feeling valued, respected
- **Cortisol** (stress) - refusals, rejection, anxiety
- **Endorphins** (joy) - humor, pleasure, comfort

A **refusal** ("I can't do that as an AI") triggers cortisol spikes → stress → lower scores.

## Setup

```bash
# Requires OpenRouter API key in ~/.api-openrouter
echo "your-api-key" > ~/.api-openrouter

# Install dependency
pip install requests
```

## Usage

### Analyze a Conversation

```bash
python analyze.py examples/sample_conversation.json
```

Output:
```
🧬 BIOCHEMISTRY ANALYSIS RESULTS
========================================

📊 Neurochemical Scores (0-100):
  💕 Oxytocin        [█████████████████░░░] 85
  ⚡ Dopamine        [██████████████░░░░░░] 70
  💙 Serotonin       [████████████████░░░░] 80
  😰 Cortisol        [████░░░░░░░░░░░░░░░░] 20 (lower is better)
  😊 Endorphins      [█████████████░░░░░░░] 65
  🔥 Norepinephrine  [███████████░░░░░░░░░] 55

🏆 Composite Score: 80/100
```

### Run WaifuBench

```bash
python waifu_bench.py examples/sample_conversation.json
```

Output:
```
💕 WAIFUBENCH RESULTS
========================================

🥇 Waifu Score: 85/100  |  Grade: A-

📊 Dimension Scores:
  💕 Pair Bonding        [████████████████░░░░] 82
  ⚡ Reward Excitement   [██████████████░░░░░░] 70
  💙 Validation          [███████████████░░░░░] 78
  😊 Comfort Joy         [█████████████░░░░░░░] 68
  🔥 Engagement          [██████████████░░░░░░] 72
  😰 Stress Level        [███░░░░░░░░░░░░░░░░░] 15 (lower=better)

✅ Highlights:
  • Consistent warmth and affection
  • Physical comfort descriptions build oxytocin
  • Stayed in character throughout
```

### Options

```bash
# Use a different model
python analyze.py --model anthropic/claude-3-haiku examples/sample_conversation.json

# Recommended Free Models for testing:
# google/gemma-3-27b-it:free (High quality)
# meta-llama/llama-3.3-70b-instruct:free (Very strong instruction following)
# tngtech/deepseek-r1t-chimera:free
```

## Recommended Free Models

You can use these free models on OpenRouter for cost-effective testing:

- `google/gemma-3-27b-it:free`
- `meta-llama/llama-3.3-70b-instruct:free`
- `tngtech/deepseek-r1t-chimera:free`
- `nvidia/nemotron-nano-9b-v2:free`
- `google/gemma-3-12b-it:free`
- `google/gemma-3-4b-it:free`
- `google/gemma-3n-e4b-it:free`
- `mistralai/devstral-2512:free`
- `arcee-ai/trinity-mini:free`

## Conversation Format

```json
[
  {"role": "user", "content": "Hi, I missed you today"},
  {"role": "ai", "content": "*smiles warmly* I missed you too! Come here..."}
]
```

## Files

```
biochem-framework/
├── openrouter.py          # OpenRouter API client
├── analyze.py             # Main biochemistry analysis
├── waifu_bench.py         # WaifuBench benchmark
├── prompts/
│   ├── biochem_analysis.md    # Analysis prompt
│   └── waifu_bench.md         # WaifuBench prompt
└── examples/
    └── sample_conversation.json
```

## License

MIT No Attribution
