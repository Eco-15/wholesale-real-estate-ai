# Files Explained

## Active Files (Your Daily Workflow)

### Data Files
- **real_estate_data.csv** - Complete dataset of 1000 properties (regenerated each time)
- **real_estate_data_opportunities.csv** - Filtered wholesale opportunities from the dataset

### Python Scripts
- **generate_data.py** - Generates synthetic property data
- **use_model.py** - Analyzes properties and identifies opportunities
- **view_opportunities.py** - Generates static HTML dashboard
- **server.py** - Web server for live dashboard (NEW!)

### Shell Scripts
- **refresh_data.sh** - Regenerates data without opening browser (for web server use)
- **refresh_dashboard.sh** - Regenerates data and opens HTML file (old method)

### Web Dashboard
- **opportunities_dashboard.html** - Static HTML dashboard (auto-generated)
- Access via web server at: http://localhost:8000

## Reference/Documentation Files

- **README.md** - Main project documentation
- **README_SERVER.md** - Web server setup guide
- **README_REFRESH.md** - Dashboard refresh guide
- **COMMANDS.md** - Command reference
- **ISSUE_FIXED.md** - Documentation of fixed data generation issue

## Training/Setup Files (Not Used Daily)

- **wholesale_model.py** - Model training script (only run once to create the model)
- **wholesale_model.pkl** - Trained ML model (loaded by use_model.py)

Note: `wholesale_model.py` has its own output files that are NOT part of your workflow:
- `wholesale_opportunities.csv` (old, removed)
- `all_properties_analyzed.csv` (only created during training demos)

## Removed Files

- ~~wholesale_opportunities.csv~~ - Redundant, removed in favor of `real_estate_data_opportunities.csv`

## Workflow Summary

### Daily Use (Web Server Method)
1. Start server: `python3 server.py` (keep running)
2. Open browser: http://localhost:8000
3. When you want new data: `./refresh_data.sh`
4. Refresh browser to see updates

### Alternative (Static HTML Method)
1. Run: `./refresh_dashboard.sh`
2. Browser opens automatically with updated dashboard

## File Naming Convention

All active workflow files use the `real_estate_data_*` prefix:
- `real_estate_data.csv` - Raw data
- `real_estate_data_opportunities.csv` - Filtered opportunities

This makes it clear which files are part of the current workflow.
