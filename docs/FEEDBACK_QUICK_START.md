# Feedback Learning - Quick Start Guide

## What Is This?

Your model gets **progressively better** as you use it in the real world. Every time a property closes or you correct a valuation, the model learns from it.

## 3-Step Process

### 1️⃣ Add Feedback (When Properties Close)

```bash
python3 src/feedback_cli.py add-feedback PROP_0123 500000 485000
```

**Format:** `property_id predicted_value actual_value`

### 2️⃣ View Progress

```bash
python3 src/feedback_cli.py summary
```

**Shows:**
- How many feedback entries collected
- Model accuracy improvement
- Deal success rate

### 3️⃣ Retrain Model (Every 10-20 entries)

```bash
python3 src/feedback_cli.py retrain
```

**Result:** Model incorporates all feedback and gets more accurate!

## Common Scenarios

### Property Just Sold

```bash
# Predicted $500k, sold for $485k
python3 src/feedback_cli.py add-feedback PROP_0123 500000 485000
```

### Wholesale Deal Closed Successfully

```bash
python3 src/feedback_cli.py add-feedback PROP_0456 650000 625000 \
  --type deal_closed \
  --outcome success \
  --notes "Buyer happy with deal"
```

### Deal Failed (Model Was Wrong)

```bash
python3 src/feedback_cli.py add-feedback PROP_0789 800000 720000 \
  --type deal_failed \
  --outcome failed \
  --notes "Appraisal revealed issues"
```

### Expert Correction

```bash
# You know the market better than the model
python3 src/feedback_cli.py add-feedback PROP_0234 1200000 1150000 \
  --type user_correction \
  --confidence 9 \
  --notes "Located on busy street, reduces value"
```

## Interactive Mode (Easier)

```bash
python3 src/feedback_cli.py add
```

Just answer the prompts - no need to remember command syntax!

## Active Learning (Smart Feedback Collection)

The model tells you which properties it's most uncertain about:

```bash
python3 src/feedback_cli.py suggest
```

**Prioritize getting feedback on these properties** - they'll improve the model most!

## Tracking Improvement

### Before Feedback
```
Model Version: 1
MAE: $18,234
R²: 0.8906
```

### After 50 Feedback Entries
```
Model Version: 4
MAE: $12,456 (31% improvement! ⬇️)
R²: 0.9312 (93% accuracy ⬆️)
```

## Best Practices

✅ **DO:**
- Add feedback for both correct and incorrect predictions
- Document uncertainty in notes
- Retrain regularly (every 10-20 entries)
- Use suggested properties for feedback
- Track deal outcomes

❌ **DON'T:**
- Only add feedback when model is wrong (creates bias)
- Skip retraining for months (model won't improve)
- Forget to document why deals failed

## Files Created

- `data/feedback_database.csv` - All your feedback entries
- `data/learning_log.json` - Model improvement history
- `models/wholesale_model.pkl.backup_*` - Backups of old models

## Why This Matters

**Traditional Model:** Static, never improves, gets outdated

**Learning Model:**
- Adapts to market changes
- Learns from your expertise
- Gets better with every deal
- Understands local market nuances

**Example:**
> Month 1: Model MAE = $18k
> Month 3: Model MAE = $14k (22% better)
> Month 6: Model MAE = $11k (39% better)
>
> **Result:** More accurate predictions = better deal identification = more profit

## Quick Commands Cheat Sheet

```bash
# Add feedback
python3 src/feedback_cli.py add

# Show stats
python3 src/feedback_cli.py summary

# Retrain model
python3 src/feedback_cli.py retrain

# Get suggestions
python3 src/feedback_cli.py suggest

# Help
python3 src/feedback_cli.py --help
```

## Integration with Workflow

1. **Morning:** Check dashboard for new opportunities
2. **During Day:** Analyze properties, make offers
3. **When Deal Closes:** Add feedback immediately
4. **Weekly:** Check summary, retrain if needed
5. **Monthly:** Review improvement metrics

## Questions?

- See `docs/REINFORCEMENT_LEARNING.md` for details
- Check `src/feedback_learning.py` for code
- Run any command with `--help` flag

---

**Start today!** Even one feedback entry helps the model learn. 🚀
