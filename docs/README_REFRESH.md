# Dashboard Refresh Guide

## Complete Workflow

When you generate new data, the dashboard needs to be updated to reflect the changes.

---

## Automatic Refresh (Recommended)

Run the automated refresh script:

```bash
./refresh_dashboard.sh
```

This single command will:
1. Generate new property data (1000 properties)
2. Analyze all properties for opportunities
3. Regenerate the dashboard with new data
4. Open the updated dashboard in your browser

---

## Manual Refresh

If you prefer to run each step manually:

```bash
# Step 1: Generate new data
python3 generate_data.py

# Step 2: Analyze for opportunities
python3 use_model.py real_estate_data.csv

# Step 3: Regenerate dashboard
python3 view_opportunities.py real_estate_data_opportunities.csv

# Step 4: Open dashboard
open opportunities_dashboard.html
```

---

## What Gets Updated

### Files Refreshed:
- **real_estate_data.csv** - Complete dataset (1000 properties)
- **real_estate_data_opportunities.csv** - Filtered opportunities
- **opportunities_dashboard.html** - Interactive dashboard

### Dashboard Shows:
- **Best Opportunities Tab**: 151 wholesale deals (with new data)
- **All Properties Tab**: All 1000 properties (newly generated)
- Updated statistics and metrics
- New property rankings

---

## When to Refresh

Refresh the dashboard when you:
- Generate new test data
- Import new real property data
- Want to see different market conditions
- Need fresh examples for analysis

---

## Quick Commands

```bash
# Full refresh
./refresh_dashboard.sh

# Just regenerate dashboard (if data already updated)
python3 view_opportunities.py real_estate_data_opportunities.csv
open opportunities_dashboard.html
```

---

## Design Notes

The dashboard features a **sleek black & white design**:
- Minimalist aesthetic
- High contrast for readability
- No emojis (clean professional look)
- Responsive layout
- Smooth transitions

---

## Troubleshooting

**Dashboard shows old data?**
- Run `./refresh_dashboard.sh` to completely refresh

**Script not executable?**
- Run: `chmod +x refresh_dashboard.sh`

**Data not updating?**
- Check timestamps: `ls -lh *.csv`
- Manually delete old CSVs and regenerate

---

The refresh workflow ensures your dashboard always shows the latest data!
