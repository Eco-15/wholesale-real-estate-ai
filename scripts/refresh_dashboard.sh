#!/bin/bash

# DASHBOARD REFRESH SCRIPT
# Generates new data, analyzes it, and updates the dashboard

echo "========================================"
echo "REFRESHING WHOLESALE DASHBOARD"
echo "========================================"
echo ""

# Step 1: Generate new data
echo "[1/3] Generating new property data..."
python3 src/generate_data.py
echo ""

# Step 2: Analyze the data
echo "[2/3] Analyzing properties for opportunities..."
python3 src/use_model.py data/real_estate_data.csv
echo ""

# Step 3: Regenerate dashboard
echo "[3/3] Regenerating dashboard..."
python3 src/view_opportunities.py data/real_estate_data_opportunities.csv
echo ""

echo "========================================"
echo "DASHBOARD REFRESH COMPLETE"
echo "========================================"
echo ""
echo "Opening dashboard in browser..."
open output/opportunities_dashboard.html
