# 🎯 COMMAND CHEAT SHEET

Quick reference for running the wholesale finder system.

---

## 🚀 First Time Setup (Run Once)

```bash
# Install required packages
pip install pandas numpy xgboost scikit-learn
```

---

## 💻 Daily Use Commands

### Analyze Properties (Most Common)
```bash
# With your own CSV file
python3 use_model.py your_properties.csv

# With demo data
python3 use_model.py
```

### View Results in Interactive Dashboard (NEW!)
```bash
# Generate beautiful web dashboard
python3 view_opportunities.py

# Or with custom data
python3 view_opportunities.py your_opportunities.csv

# Opens in your browser automatically!
```

### Generate Test Data
```bash
python3 generate_data.py
```

### Train New Model (Advanced)
```bash
python3 wholesale_model.py
```

---

## 📊 Python Script Usage

### Analyze Your Data
```python
from wholesale_model import RealEstateWholesaleModel
import pandas as pd

# Load model
model = RealEstateWholesaleModel()
model.load_model('wholesale_model.pkl')

# Load your properties
df = pd.read_csv('your_properties.csv')

# Find opportunities
opportunities, results = model.find_opportunities(
    df,
    min_spread=20000,      # Minimum $20k spread
    min_spread_pct=10      # Minimum 10% spread
)

# Save results
opportunities.to_csv('my_opportunities.csv', index=False)
```

### Train on Your Market
```python
from wholesale_model import RealEstateWholesaleModel
import pandas as pd

# Load your market data
df = pd.read_csv('my_market_data.csv')

# Train new model
model = RealEstateWholesaleModel()
model.train(df)

# Save for later use
model.save_model('my_market_model.pkl')

# Find opportunities
opportunities, results = model.find_opportunities(df)
```

---

## 🔧 Customization Examples

### Lower Standards (Find More Deals)
```python
opportunities, results = model.find_opportunities(
    df,
    min_spread=10000,      # Was 20000
    min_spread_pct=5       # Was 10
)
```

### Filter by Neighborhood
```python
# After getting opportunities
downtown_deals = opportunities[
    opportunities['neighborhood'] == 'Downtown'
]
```

### Focus on Distressed Properties
```python
# High distress score = motivated sellers
hot_leads = opportunities[
    opportunities['distress_score'] > 50
]
```

### Only Foreclosures
```python
foreclosures = opportunities[
    opportunities['is_foreclosure'] == 1
]
```

---

## 📂 File Operations

### Check What You Have
```bash
ls -lh *.csv *.pkl *.py
```

### View First 10 Opportunities
```bash
head -n 10 wholesale_opportunities.csv
```

### Count Total Opportunities
```bash
wc -l wholesale_opportunities.csv
```

### Open in Excel/Numbers
```bash
# Mac
open wholesale_opportunities.csv

# Windows
start wholesale_opportunities.csv

# Linux
xdg-open wholesale_opportunities.csv
```

---

## 🔍 Quick Data Checks

### Python Quick Analysis
```python
import pandas as pd

# Load results
df = pd.read_csv('wholesale_opportunities.csv')

# Show top 10
print(df.head(10))

# Summary stats
print(f"Total opportunities: {len(df)}")
print(f"Avg spread: ${df['predicted_spread'].mean():,.0f}")
print(f"Avg profit: ${df['estimated_profit'].mean():,.0f}")

# Best deals
best = df.nlargest(5, 'opportunity_score')
print(best[['property_id', 'listed_price', 'predicted_spread', 'opportunity_score']])
```

### Bash Quick Stats
```bash
# Count opportunities
wc -l wholesale_opportunities.csv

# Show just property IDs and scores
cut -d',' -f1,17 wholesale_opportunities.csv | head -20
```

---

## 🎯 Workflow Commands

### Daily Analysis Workflow
```bash
# 1. Export new properties from PropStream to properties_nov3.csv

# 2. Run analysis
python use_model.py properties_nov3.csv

# 3. Results saved to properties_nov3_opportunities.csv

# 4. Open in spreadsheet
open properties_nov3_opportunities.csv

# 5. Contact top 10 leads!
```

### Weekly Market Analysis
```bash
# Get all week's data
cat properties_day*.csv > properties_week.csv

# Analyze
python use_model.py properties_week.csv

# Compare to last week
python -c "
import pandas as pd
this_week = pd.read_csv('properties_week_opportunities.csv')
last_week = pd.read_csv('properties_lastweek_opportunities.csv')
print(f'This week: {len(this_week)} opportunities')
print(f'Last week: {len(last_week)} opportunities')
print(f'Change: {len(this_week) - len(last_week)}')
"
```

---

## 🔄 Model Management

### Save Current Model
```python
model.save_model('backup_model_nov3.pkl')
```

### Load Specific Model
```python
model.load_model('my_market_model.pkl')
```

### Compare Models
```python
# Load both models
model1 = RealEstateWholesaleModel()
model1.load_model('model_v1.pkl')

model2 = RealEstateWholesaleModel()
model2.load_model('model_v2.pkl')

# Test on same data
pred1 = model1.predict(test_data)
pred2 = model2.predict(test_data)

# Compare
from sklearn.metrics import mean_absolute_error
mae1 = mean_absolute_error(actual_values, pred1)
mae2 = mean_absolute_error(actual_values, pred2)
print(f"Model 1 MAE: ${mae1:,.0f}")
print(f"Model 2 MAE: ${mae2:,.0f}")
```

---

## 📧 Export for Email/CRM

### Create Email List
```python
import pandas as pd

opps = pd.read_csv('wholesale_opportunities.csv')

# Top 20 for cold calling
top20 = opps.head(20)[['property_id', 'neighborhood', 'bedrooms', 
                        'bathrooms', 'listed_price', 'predicted_spread']]

top20.to_csv('todays_leads.csv', index=False)
```

### Create Mailchimp Import
```python
# Format for email marketing
email_list = opps.head(50)[['property_id', 'neighborhood', 'listed_price']]
email_list.to_csv('mailchimp_import.csv', index=False)
```

---

## 🐛 Troubleshooting Commands

### Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

### Check Installed Packages
```bash
pip list | grep -E "pandas|numpy|xgboost|scikit"
```

### Reinstall Everything
```bash
pip uninstall pandas numpy xgboost scikit-learn -y
pip install pandas numpy xgboost scikit-learn
```

### Test Installation
```python
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
print("✅ All packages working!")
```

### Verify Model File
```bash
# Check if model exists and size
ls -lh wholesale_model.pkl

# Try loading it
python -c "import pickle; pickle.load(open('wholesale_model.pkl', 'rb')); print('✅ Model loads OK')"
```

---

## 📊 Performance Testing

### Benchmark Speed
```python
import time
import pandas as pd
from wholesale_model import RealEstateWholesaleModel

# Load model
model = RealEstateWholesaleModel()
model.load_model('wholesale_model.pkl')

# Load data
df = pd.read_csv('real_estate_data.csv')

# Time prediction
start = time.time()
predictions = model.predict(df)
end = time.time()

print(f"Predicted {len(df)} properties in {end-start:.2f} seconds")
print(f"Speed: {len(df)/(end-start):.0f} properties/second")
```

### Memory Usage
```python
import sys
import pickle

model_data = pickle.load(open('wholesale_model.pkl', 'rb'))
size_bytes = sys.getsizeof(pickle.dumps(model_data))
size_mb = size_bytes / (1024 * 1024)
print(f"Model size: {size_mb:.2f} MB")
```

---

## 🎓 Learning Commands

### Explore the Data
```python
import pandas as pd

df = pd.read_csv('real_estate_data.csv')

# Basic info
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# See distributions
print(df['condition'].value_counts())
print(df['neighborhood'].value_counts())
```

### Understand Feature Importance
```python
from wholesale_model import RealEstateWholesaleModel

model = RealEstateWholesaleModel()
model.load_model('wholesale_model.pkl')

# Get feature importance
import pandas as pd
importance_df = pd.DataFrame({
    'feature': model.feature_columns,
    'importance': model.model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance_df)
```

---

## 💾 Backup & Version Control

### Backup Everything
```bash
# Create backup folder
mkdir backup_$(date +%Y%m%d)

# Copy all files
cp *.py *.pkl *.csv *.md backup_$(date +%Y%m%d)/

# Or create zip
zip -r wholesale_backup_$(date +%Y%m%d).zip *.py *.pkl *.csv *.md
```

### Git Version Control (Optional)
```bash
git init
git add *.py *.md
git commit -m "Initial wholesale finder system"

# Don't commit large CSV files or models
echo "*.csv" >> .gitignore
echo "*.pkl" >> .gitignore
```

---

## 🚀 Automation Scripts

### Daily Analysis Script (save as run_daily.sh)
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)

# Download from PropStream (replace with your method)
# ... your download script here ...

# Run analysis
python use_model.py properties_$DATE.csv

# Email results (requires mail setup)
echo "Found opportunities - see attachment" | mail -s "Daily Wholesale Report" -a properties_${DATE}_opportunities.csv you@email.com

echo "✅ Daily analysis complete!"
```

### Make executable and run
```bash
chmod +x run_daily.sh
./run_daily.sh
```

### Scheduled with cron (Mac/Linux)
```bash
# Run daily at 9 AM
crontab -e

# Add this line:
0 9 * * * cd /path/to/wholesale && ./run_daily.sh
```

---

## 📱 Quick Commands Reference

| Task | Command |
|------|---------|
| Analyze properties | `python use_model.py data.csv` |
| Generate test data | `python generate_data.py` |
| Train new model | `python wholesale_model.py` |
| View results | `open wholesale_opportunities.csv` |
| Quick stats | `wc -l *.csv` |
| Install packages | `pip install pandas numpy xgboost scikit-learn` |

---

## 🎯 Remember

**Most common command you'll use:**
```bash
python use_model.py your_properties.csv
```

That's it! Everything else is optional customization.

---

**Keep this file handy for quick reference!** 📌
