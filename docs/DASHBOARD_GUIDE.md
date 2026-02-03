# 📊 Wholesale Opportunities Dashboard Guide

Quick guide to using the interactive dashboard for analyzing wholesale real estate opportunities.

---

## 🚀 Quick Start

### Generate Dashboard
```bash
# After running analysis
python3 view_opportunities.py

# Or with custom data
python3 view_opportunities.py your_opportunities.csv
```

### Open Dashboard
```bash
open opportunities_dashboard.html
```

The dashboard will open in your default web browser.

---

## 📱 Dashboard Features

### 1. **Overview Statistics** (Top Cards)
At the top of the dashboard, you'll see key metrics:
- **Total Opportunities**: Number of wholesale deals found
- **Avg Spread**: Average difference between market value and listed price
- **Avg Profit**: Average profit after repair costs
- **Total Potential**: Sum of all potential profits

### 2. **Filters & Controls**
Use the control panel to narrow down opportunities:

#### Search
- Search by property ID, neighborhood, or address
- Press Enter or click "Apply Filters"

#### Condition Filter
- Excellent
- Good
- Fair
- Poor
- Distressed

#### Property Type Filter
- Single Family
- Condo
- Townhouse
- Multi-Family

#### Min Profit
- Set minimum profit threshold (e.g., 50000 for $50k)
- Filters out deals below this amount

#### Sort By
- **Opportunity Score** (default) - Best overall deals
- **Estimated Profit** - Highest profit potential
- **Predicted Spread** - Largest spread in dollars
- **Spread Percentage** - Best percentage returns
- **Distress Score** - Most motivated sellers
- **Days on Market** - Longest listings

### 3. **Property Cards**
Each property card shows:
- **Rank**: Position in sorted list
- **Score**: Opportunity score (0-100)
- **Property ID**: Unique identifier
- **Location**: Neighborhood and property type
- **Key Metrics**:
  - Listed Price
  - Market Value
  - Spread (highlighted in green)
  - Estimated Profit (highlighted in green)
  - Size (beds/baths)
  - Square Footage
- **Tags**:
  - Condition badge (color-coded)
  - Foreclosure indicator
  - High distress indicator
  - Days on market
  - Price reductions

### 4. **Detailed View**
Click any property card to see full details:

#### Financial Overview
- Complete pricing breakdown
- Spread percentage
- Visual profit calculation

#### Profit Breakdown
Color-coded section showing:
- Market Value
- Listed Price (subtracted)
- Repair Costs (subtracted)
- **Final Estimated Profit**

#### Property Details
- Bedrooms, Bathrooms
- Square Feet, Lot Size
- Year Built, Age
- Condition
- Property Type

#### Motivation Indicators
- **Distress Score**: Higher = more motivated seller
- **Days on Market**: Longer = more negotiable
- **Price Reductions**: More cuts = motivated
- **Foreclosure**: Yes/No
- **Has Lien**: Yes/No
- **Owner Occupied**: Yes/No
- **Opportunity Score**: Overall deal quality

---

## 💡 How to Use

### Finding Top Deals
1. Default view shows properties sorted by **Opportunity Score**
2. Top 10 deals are usually your best bets
3. Look for:
   - High opportunity scores (70+)
   - Good profit margins ($50k+)
   - High distress scores (motivated sellers)
   - Multiple price reductions

### Finding Motivated Sellers
1. Sort by **Distress Score**
2. Look for:
   - Foreclosures
   - Properties with liens
   - Long days on market (100+)
   - Multiple price reductions
   - Distressed condition

### Finding High-Profit Deals
1. Sort by **Estimated Profit**
2. Set Min Profit filter (e.g., 75000)
3. Check repair costs are reasonable
4. Verify spread percentage is healthy (15%+)

### Finding Quick Flips
1. Filter by Condition: "Excellent" or "Good"
2. Sort by **Estimated Profit**
3. Low repair costs = faster turnaround
4. Look for properties with good spread

### Finding Specific Markets
1. Use Search to find neighborhoods
2. Filter by Property Type
3. Review all matching properties
4. Compare metrics across area

---

## 🎯 Understanding the Metrics

### Opportunity Score (0-100)
Composite score combining:
- Spread percentage
- Distress indicators
- Days on market
- Price reductions
- Overall deal quality

**Higher is better** - Scores above 70 are excellent deals

### Distress Score (0-100)
Indicates seller motivation based on:
- Foreclosure status
- Liens
- Days on market
- Price reductions
- Property condition
- Distress keywords

**Higher = More Motivated Seller**

### Spread
Difference between market value and listed price
- **Dollar Amount**: Total spread
- **Percentage**: Return on purchase price

Good deals: 15%+ spread

### Estimated Profit
Final profit after deducting:
- Purchase price (listed price)
- Estimated repair costs
- From predicted market value

This is your wholesale fee potential

---

## 🔧 Tips & Tricks

### Keyboard Shortcuts
- **Escape**: Close property detail modal
- **Enter**: Apply filters (when in search box)

### Best Practices
1. **Start with defaults** - Opportunity score shows best overall deals
2. **Use filters to narrow** - Don't get overwhelmed by all properties
3. **Click for details** - Always review full details before pursuing
4. **Check distress indicators** - High distress = easier negotiations
5. **Verify repair costs** - Built-in estimates may vary from reality

### Red Flags to Watch
- Very high repair costs (40%+ of spread)
- Low spread percentage (<10%)
- Property sitting for 200+ days with no price cuts
- Excellent condition but high distress (verify data)

### Green Flags to Seek
- Multiple price reductions
- 60+ days on market
- Foreclosure or lien
- Fair/Poor condition with manageable repairs
- High spread percentage (20%+)
- Opportunity score 75+

---

## 🔄 Refreshing Data

After running new analysis:
```bash
# Run analysis on new data
python3 use_model.py new_properties.csv

# Generate new dashboard
python3 view_opportunities.py new_properties_opportunities.csv

# Open updated dashboard
open opportunities_dashboard.html
```

The browser will load the latest data.

---

## 📤 Exporting Data

The dashboard works with CSV files. To export filtered results:

1. Use the dashboard to find your criteria
2. Note your filter settings
3. Use Python to export:

```python
import pandas as pd

# Load data
df = pd.read_csv('wholesale_opportunities.csv')

# Apply same filters
filtered = df[
    (df['estimated_profit'] >= 50000) &
    (df['condition'] == 'Fair')
]

# Export
filtered.to_csv('my_leads.csv', index=False)
```

---

## 🎨 Color Coding

### Condition Badges
- 🟢 **Green**: Excellent
- 🔵 **Blue**: Good
- 🟡 **Yellow**: Fair
- 🔴 **Light Red**: Poor
- 🔴 **Dark Red**: Distressed

### Profit Metrics
- **Green numbers**: Profit and spread (good things)
- **Purple/Blue**: Opportunity scores
- **Gray**: Neutral information

---

## 🐛 Troubleshooting

### Dashboard shows "No properties found"
- Check that CSV file exists
- Verify CSV has data
- Try resetting filters
- Regenerate dashboard: `python3 view_opportunities.py`

### Dashboard won't open
- Check file was created: `ls -l opportunities_dashboard.html`
- Manually double-click the HTML file
- Try: `open opportunities_dashboard.html`

### Data looks wrong
- Verify correct CSV file was used
- Re-run analysis: `python3 use_model.py`
- Regenerate dashboard: `python3 view_opportunities.py`

### Filters not working
- Click "Apply Filters" after changing settings
- Try "Reset" button to clear all filters
- Refresh browser page

---

## 📱 Mobile Support

The dashboard is responsive and works on:
- Desktop browsers (Chrome, Safari, Firefox, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iPhone, Android)

On mobile:
- Cards stack vertically
- Filters become full-width
- Modal details are scrollable

---

## 🚀 Workflow Example

### Daily Analysis Workflow

1. **Get new properties**
   ```bash
   # Export from PropStream/MLS to properties_today.csv
   ```

2. **Run analysis**
   ```bash
   python3 use_model.py properties_today.csv
   ```

3. **Generate dashboard**
   ```bash
   python3 view_opportunities.py properties_today_opportunities.csv
   ```

4. **Review in browser**
   - Sort by Opportunity Score
   - Filter Min Profit: 50000
   - Review top 10 deals

5. **Deep dive on winners**
   - Click each property
   - Check distress indicators
   - Verify repair costs
   - Note property IDs for outreach

6. **Export leads**
   - Note top 5-10 property IDs
   - Use for calling/mailing campaign

---

## 💾 Saving Your Workflow

### Create a bash script: `daily_analysis.sh`
```bash
#!/bin/bash

# Daily wholesale analysis
DATE=$(date +%Y%m%d)
INPUT="properties_${DATE}.csv"

echo "🏠 Daily Wholesale Analysis"
echo "=========================="

# Run analysis
python3 use_model.py "$INPUT"

# Generate dashboard
python3 view_opportunities.py "${INPUT%.csv}_opportunities.csv"

# Open in browser
open opportunities_dashboard.html

echo "✅ Complete! Dashboard is open."
```

Make executable:
```bash
chmod +x daily_analysis.sh
```

Run daily:
```bash
./daily_analysis.sh
```

---

## 🎯 Remember

The dashboard is a **decision support tool**:
- ✅ Use it to quickly identify promising deals
- ✅ Use it to filter and sort large datasets
- ✅ Use it to understand deal metrics
- ⚠️ Always verify data with actual property research
- ⚠️ Repair costs are estimates - get real quotes
- ⚠️ Model predictions should be validated

**Trust but verify!** Use the dashboard to find leads, then do your due diligence.

---

**Happy Deal Finding!** 🏠💰
