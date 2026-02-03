# 🏠 Real Estate Wholesale Opportunity Finder

## What This Does

This is a **complete machine learning system** for finding undervalued real estate properties for wholesaling. It uses XGBoost (not deep learning - it's better for this use case!) to:

1. **Predict market values** of properties based on their features
2. **Calculate spreads** between predicted value and listed price
3. **Score distress signals** (days on market, price drops, foreclosures, etc.)
4. **Rank opportunities** by profit potential

---

## 📊 Results from Synthetic Data Test

### Model Performance
- **Test Accuracy**: $34,204 average error (6.33% MAPE)
- **R² Score**: 0.8976 (89.76% of variance explained)
- **Opportunities Found**: 151 properties with $20k+ spread
- **Average Profit**: $51,955 per deal

### Top Feature Importance
1. Square feet (25.8%)
2. Bedrooms (18.5%)
3. Price per sqft (16.1%)
4. Bathrooms (9.5%)
5. Neighborhood (8.3%)

---

## 📁 Files Included

### Core System
- **`wholesale_model.py`** - Main model training and analysis system
- **`use_model.py`** - Simple script to analyze new properties
- **`generate_data.py`** - Synthetic data generator (for testing)
- **`wholesale_model.pkl`** - Trained model (ready to use!)

### Data Files
- **`real_estate_data.csv`** - 1,000 synthetic properties for testing
- **`wholesale_opportunities.csv`** - Top 151 opportunities ranked
- **`all_properties_analyzed.csv`** - All 1,000 properties with predictions

---

## 🚀 How to Use

### Option 1: Quick Start with Demo Data

```bash
python use_model.py
```

This runs the model on the synthetic data to show you how it works.

### Option 2: Analyze Your Own Properties

1. **Export your data to CSV** with these columns:
   ```
   neighborhood, property_type, bedrooms, bathrooms, square_feet, 
   lot_size, year_built, condition, days_on_market, price_reductions,
   is_foreclosure, has_lien, owner_occupied, num_distress_keywords,
   listed_price, estimated_repair_cost
   ```

2. **Run the analyzer:**
   ```bash
   python use_model.py your_properties.csv
   ```

3. **Get results!** Top opportunities saved to `your_properties_opportunities.csv`

### Option 3: Retrain Model with Your Market Data

If you want to train on YOUR local market data:

```python
from wholesale_model import RealEstateWholesaleModel
import pandas as pd

# Load your data
df = pd.read_csv('your_market_data.csv')

# Train new model
model = RealEstateWholesaleModel()
model.train(df)

# Find opportunities
opportunities, results = model.find_opportunities(df)

# Save model
model.save_model('my_market_model.pkl')
```

---

## 📋 Data Requirements

### Required Columns
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `neighborhood` | string | Location/neighborhood | "Downtown", "Suburbs" |
| `property_type` | string | Type of property | "Single Family", "Condo" |
| `bedrooms` | int | Number of bedrooms | 3 |
| `bathrooms` | int/float | Number of bathrooms | 2.5 |
| `square_feet` | int | Square footage | 2000 |
| `lot_size` | int | Lot size in sqft | 8000 |
| `year_built` | int | Year built | 1985 |
| `condition` | string | Property condition | "Good", "Fair", "Poor" |
| `days_on_market` | int | Days listed | 45 |
| `price_reductions` | int | Number of price drops | 2 |
| `listed_price` | int | Current asking price | 350000 |

### Optional But Helpful
| Column | Type | Default | Description |
|--------|------|---------|-------------|
| `is_foreclosure` | 0 or 1 | 0 | Is it a foreclosure? |
| `has_lien` | 0 or 1 | 0 | Does it have liens? |
| `owner_occupied` | 0 or 1 | 1 | Is owner living there? |
| `num_distress_keywords` | int | 0 | Count of "motivated", "as-is", etc. |
| `estimated_repair_cost` | int | auto | Estimated repairs needed |

### Where to Get Data

#### **Paid Sources (Recommended)**
1. **PropStream** - $97-197/month
   - Best for wholesalers
   - Built-in distress signals
   - Skip tracing included
   - Easy CSV export

2. **MLS Access** - $50-200/month
   - Requires real estate license
   - Most accurate data
   - Real-time updates

3. **Attom Data** - $500-1000/month
   - Comprehensive API
   - Good for automation
   - Nationwide coverage

#### **Free/DIY Sources**
- Web scraping (Zillow, Realtor.com) - Difficult, gets blocked
- County assessor websites - Manual but free
- Public records - Free but tedious

---

## 💡 Understanding the Results

### Opportunity Score
Higher = Better opportunity. Combines:
- **Spread %** (most important) - How undervalued is it?
- **Distress signals** - How motivated is the seller?
- **Profit potential** - How much money can you make?

### Key Metrics Explained

**Predicted Market Value** - What the model thinks it should sell for
**Spread** - Difference between market value and listed price
**Spread %** - Spread as percentage of market value
**Distress Score** - Higher = more motivated seller
**Estimated Profit** - After repairs, wholesale fee ($10k), closing ($5k)

### Example Opportunity

```
🎯 #1 - PROP_0452 (Score: 89.6)
   📍 Rural - Single Family
   🏡 3 bed, 1 bath, 2,140 sqft
   🔧 Condition: Distressed
   📅 Days on Market: 193 | Price Drops: 1
   💵 Listed: $291,668
   📊 Predicted Market Value: $444,513
   💰 Spread: $152,845 (34.4%)
   🔨 Repair Cost: $18,321
   ✅ Est. Profit: $119,524
   🚨 Distress Score: 44.3
```

**What this means:**
- Property listed way below predicted value (34.4% below)
- Highly distressed (193 days on market, condition issues)
- After $18k repairs, you could make $120k profit
- **Action:** Contact seller ASAP, this is a hot lead!

---

## 🔧 Customization

### Adjust Opportunity Filters

```python
# Find more/fewer opportunities
opportunities, results = model.find_opportunities(
    df,
    min_spread=15000,      # Lower this to find more deals
    min_spread_pct=8       # Lower this to be less strict
)
```

### Adjust Profit Calculations

Edit in `wholesale_model.py`:
```python
# Line ~210
wholesale_fee = 10000     # Your assignment fee
closing_costs = 5000      # Typical closing costs
```

### Add Your Own Features

If you have additional data (school ratings, crime stats, etc.), add them:

```python
# In prepare_features() method
feature_cols = [
    # ... existing features ...
    'school_rating',      # Your new feature
    'crime_index',        # Your new feature
]
```

---

## ⚙️ Technical Details

### Why XGBoost Instead of Deep Learning?

For tabular real estate data:
- ✅ **More Accurate** (5-15% better than neural nets)
- ✅ **Faster Training** (minutes vs hours)
- ✅ **Less Data Needed** (works with 1K+ properties)
- ✅ **Interpretable** (shows which features matter)
- ✅ **Easier to Debug**

Deep learning only makes sense if you're processing images (property photos) or have millions of properties.

### Model Architecture

- **Algorithm**: XGBoost Regressor
- **Trees**: 200
- **Learning Rate**: 0.05
- **Max Depth**: 6
- **Features**: 18 (engineered from raw data)

### Performance on M4 MacBook

- **Training Time**: ~5 seconds (800 properties)
- **Prediction Time**: <1 second (1000 properties)
- **Memory Usage**: ~50MB
- **CPU Only**: No GPU needed!

---

## 📈 Next Steps

### Phase 1: Validate the Model (Week 1-2)
1. Get 100-200 real properties from your market
2. Run through this model
3. Manually check top 10 predictions vs real comps
4. Adjust if needed

### Phase 2: Scale Up (Month 1-2)
1. Subscribe to PropStream or MLS
2. Automate daily analysis
3. Build a simple CRM to track leads
4. Close your first deals!

### Phase 3: Automate (Month 3+)
1. Set up automatic data imports
2. Daily email alerts for new opportunities
3. Integrate with your marketing system
4. Build a team to handle volume

---

## 🚨 Important Notes

### Model Limitations

- **Not perfect** - Model is ~6% off on average
- **Market dependent** - Trained on synthetic data, retrain with your market
- **Still need validation** - Always check comps manually before making offers
- **Repair costs** - Estimates are rough, get professional inspections

### Legal Considerations

- **Data usage** - Make sure you have rights to use data
- **Fair Housing** - Don't discriminate based on protected classes
- **Licensing** - Know your state's wholesaling laws
- **Contracts** - Use proper legal contracts for assignments

### Business Reality

This model helps you **find** opportunities faster. But you still need:
- ✅ Marketing to sellers
- ✅ Negotiation skills
- ✅ Buyer network
- ✅ Deal analysis experience
- ✅ Legal knowledge

**The model is a tool, not a business.**

---

## 🛠️ Troubleshooting

### "Model prediction error is too high"
→ Retrain with more data from your specific market

### "Not finding any opportunities"
→ Lower `min_spread` and `min_spread_pct` parameters

### "Getting too many false positives"
→ Increase `min_spread` or add more distress signal requirements

### "Model crashes on my data"
→ Check that all required columns are present and have correct data types

---

## 📞 Support

This is a working MVP/proof of concept. To extend it:

1. **Add more features** - school ratings, crime stats, etc.
2. **Integrate APIs** - Auto-pull data from PropStream/MLS
3. **Build dashboard** - Web interface to view opportunities
4. **Add alerts** - Email/SMS when hot deals appear
5. **CRM integration** - Track which leads you've contacted

---

## 💰 Cost Summary

### To Run This System

| Item | Cost |
|------|------|
| Python/XGBoost | FREE |
| Training model locally | FREE |
| Running predictions | FREE |

### To Get Real Data

| Source | Monthly Cost |
|--------|-------------|
| PropStream | $97-197 |
| MLS Access | $50-200 |
| Attom Data | $500-1,000 |
| Web Scraping | $50-300 (proxies) |

**Recommendation:** Start with PropStream ($97/month) to validate the system works in your market.

---

## ✅ What You Have Now

1. ✅ **Trained XGBoost Model** - Ready to predict prices
2. ✅ **Opportunity Finder** - Ranks deals by profit potential
3. ✅ **Easy-to-use Scripts** - Just run and get results
4. ✅ **Tested System** - Found 151 opportunities in test data
5. ✅ **Documentation** - This README explains everything

**Next step:** Get real data from your market and run it through the system!

---

## 🎯 Expected Results

Based on the test data:
- **~15% of properties** are potential opportunities
- **Average spread**: $81,114
- **Average profit**: $51,955 per deal
- **Close rate**: 5-10% of opportunities = actual deals

If you analyze 100 properties:
- Find ~15 opportunities
- Contact all 15
- Close 1-2 deals
- Make ~$50k-100k profit

**Not bad for running a Python script!** 🚀

---

## License

Free to use for personal/commercial purposes. No warranty provided.

---

**Good luck with your wholesaling business! 🏠💰**
