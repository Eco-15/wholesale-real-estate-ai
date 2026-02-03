# Quick Reference Card

## Daily Commands

```bash
# Start server (keep this running)
./start_server.sh

# Refresh data (run when you want new data)
./refresh.sh
```

Then visit: **http://localhost:8000**

## Project Structure

```
src/        → Python code
scripts/    → Shell scripts
data/       → CSV files
models/     → ML models
output/     → Generated HTML
docs/       → Documentation
```

## Important Files

| File | What It Does |
|------|-------------|
| `src/server.py` | Web server |
| `src/generate_data.py` | Creates property data |
| `src/use_model.py` | Finds opportunities |
| `src/view_opportunities.py` | Creates dashboard |
| `data/real_estate_data.csv` | All properties |
| `data/real_estate_data_opportunities.csv` | Filtered deals |
| `output/opportunities_dashboard.html` | Dashboard file |

## Workflow

1. Start: `./start_server.sh`
2. Visit: http://localhost:8000
3. Refresh data: `./refresh.sh`
4. Reload browser: Press F5 or Cmd+R

## Troubleshooting

**Server won't start?**
```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9
./start_server.sh
```

**Data not updating?**
```bash
# Make sure you refreshed the browser after running refresh
./refresh.sh
# Then press Cmd+R in browser
```

**Need to edit code?**
- All Python files are in `src/`
- Edit and save, Flask auto-reloads

**Want to see static HTML?**
```bash
./scripts/refresh_dashboard.sh  # Opens in browser
```

## API Endpoints

- `http://localhost:8000` - Dashboard UI
- `http://localhost:8000/api/data` - JSON data
- `http://localhost:8000/api/refresh` - Trigger refresh

## Directory Access

From root directory:
```bash
cd src/          # Edit code
cd data/         # View data
cd output/       # Check output
cd scripts/      # Run scripts
cd docs/         # Read docs
```

---

**Everything you need on one page!** 📋
