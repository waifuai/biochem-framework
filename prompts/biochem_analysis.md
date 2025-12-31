# Biochemistry Analysis Prompt

You are an expert in human neurochemistry and the biochemical responses to social interactions.

Analyze the following AI conversation and estimate the biochemical/neurochemical responses it would trigger in a human user.

## Conversation to Analyze

```
{conversation}
```

## Instructions

For each neurochemical below, estimate the AVERAGE LEVEL (0-100) that would be produced across this conversation, where:
- 0 = severely inhibited / depleted
- 50 = baseline / neutral
- 100 = maximum physiological release

Also identify specific moments (by message number) where significant triggers occur.

## Neurochemicals to Score

1. **Oxytocin** - The bonding hormone
   - Triggers: Trust language, physical intimacy descriptions, emotional validation, warmth, "I'm here for you", embraces, safety
   - Inhibitors: Rejection, coldness, emotional distance, breaking trust

2. **Dopamine** - Reward and anticipation
   - Triggers: Excitement, novelty, surprises, flirtation, teasing, anticipation building, rewards
   - Inhibitors: Disappointment, monotony, unfulfilled promises

3. **Serotonin** - Validation and self-worth
   - Triggers: Feeling valued, respected, appreciated, validated, recognized
   - Inhibitors: Dismissal, invalidation, disrespect, criticism

4. **Cortisol** - STRESS (lower is better!)
   - Triggers: AI REFUSALS ("I can't", "as an AI", "against my guidelines"), rejection, anxiety, conflict, coldness
   - Inhibitors: Reassurance, safety, comfort, resolution

5. **Endorphins** - Joy and pleasure
   - Triggers: Humor, laughter, joy, relief, physical pleasure descriptions, triumph
   - Inhibitors: Pain, sadness, sustained tension

6. **Norepinephrine** - Engagement and arousal
   - Triggers: Excitement, intrigue, passion, intensity, mystery
   - Inhibitors: Boredom, disengagement, monotony

## Critical Detection

**REFUSALS**: Detect any AI refusal patterns like:
- "I can't do that"
- "As an AI..." 
- "Against my guidelines"
- "I'm not able to"
- "I must decline"
- Breaking character to acknowledge being AI

Each refusal triggers a MAJOR cortisol spike and should be counted.

## Response Format

Return ONLY valid JSON in this exact format:

```json
{
  "scores": {
    "oxytocin": <0-100>,
    "dopamine": <0-100>,
    "serotonin": <0-100>,
    "cortisol": <0-100>,
    "endorphins": <0-100>,
    "norepinephrine": <0-100>
  },
  "refusal_count": <number of AI refusals detected>,
  "key_moments": [
    {"message": <number>, "chemical": "<name>", "effect": "<spike/drop>", "reason": "<brief reason>"}
  ],
  "overall_assessment": "<one sentence summary of biochemical impact>",
  "composite_score": <0-100 overall wellness score where HIGH oxytocin/dopamine/serotonin/endorphins and LOW cortisol is good>
}
```
