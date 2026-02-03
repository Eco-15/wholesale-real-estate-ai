# Project Folder Structure

The project has been reorganized into a clean, professional structure.

## New Organization

```
Wholesale Deep NN/
│
├── 📁 src/                          # All Python source code
│   ├── server.py                   # Web server (Flask)
│   ├── generate_data.py            # Generate synthetic data
│   ├── use_model.py                # Analyze properties
│   ├── view_opportunities.py       # Generate dashboard HTML
│   └── wholesale_model.py          # Train ML model
│
├── 📁 scripts/                      # Shell scripts
│   ├── refresh_data.sh            # Refresh data (for web server)
│   └── refresh_dashboard.sh       # Refresh & open HTML
│
├── 📁 data/                         # CSV data files
│   ├── real_estate_data.csv       # All 1000 properties
│   └── real_estate_data_opportunities.csv  # 106 opportunities
│
├── 📁 models/                       # Trained ML models
│   └── wholesale_model.pkl        # XGBoost model
│
├── 📁 output/                       # Generated files
│   └── opportunities_dashboard.html
│
├── 📁 docs/                         # Documentation
│   ├── README.md                  # Main docs (moved from root)
│   ├── COMMANDS.md                # Command reference
│   ├── README_SERVER.md           # Server setup guide
│   ├── README_REFRESH.md          # Refresh guide
│   ├── FILES_EXPLAINED.md         # File explanations
│   ├── DASHBOARD_*.md             # Dashboard docs
│   └── ... (other docs)
│
├── 📄 README.md                     # Quick start guide (NEW)
├── 🚀 start_server.sh               # Start web server
└── 🔄 refresh.sh                    # Refresh data
```

## Why This Structure?

### Before (Messy)
```
- All files mixed together in root
- Hard to find what you need
- Python, docs, data all jumbled
- 28 files in one directory
```

### After (Clean)
```
- Source code in src/
- Data files in data/
- Output in output/
- Docs in docs/
- Easy wrapper scripts in root
- Professional organization
```

## Quick Access

### Start Working
```bash
./start_server.sh          # Start server
./refresh.sh               # Refresh data
```

### Find Things
- **Need to edit code?** → `src/`
- **Looking for data?** → `data/`
- **Want docs?** → `docs/`
- **Check output?** → `output/`
- **Run scripts?** → `scripts/` (or use wrappers in root)

## File Paths Updated

All scripts and Python files now use proper paths:
- `data/real_estate_data.csv`
- `models/wholesale_model.pkl`
- `output/opportunities_dashboard.html`

No more confusion about where files are!

## Benefits

1. **Clean root directory** - Only essential files
2. **Easy to navigate** - Logical folder names
3. **Scalable** - Add files to appropriate folders
4. **Professional** - Industry-standard structure
5. **No path confusion** - Everything in its place

## Migration Complete

✅ All Python files moved to `src/`
✅ All shell scripts moved to `scripts/`
✅ All data files moved to `data/`
✅ All docs moved to `docs/`
✅ Model moved to `models/`
✅ Output moved to `output/`
✅ All paths updated in code
✅ Wrapper scripts created
✅ New README written
✅ Server tested and working

**Your project is now professionally organized!** 🎉
