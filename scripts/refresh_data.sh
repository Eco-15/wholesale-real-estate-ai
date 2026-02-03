#!/bin/bash

# DATA REFRESH SCRIPT (For use with web server)
# Processes real data and analyzes it WITHOUT opening browser

echo "========================================"
echo "REFRESHING DATA"
echo "========================================"
echo ""

# Step 1: Process real data with random property count (250-500)
echo "[1/3] Generating new property data..."
python3 src/process_real_data.py
echo ""

# Step 2: Analyze the data
echo "[2/3] Analyzing properties for opportunities..."
python3 src/use_model.py data/real_estate_data.csv
echo ""

# Step 3: Regenerate dashboard HTML
echo "[3/3] Regenerating dashboard HTML..."
python3 src/view_opportunities.py data/real_estate_data_opportunities.csv
echo ""

echo "========================================"
echo "DATA REFRESH COMPLETE"
echo "========================================"
echo ""
echo "If using web server, just refresh your browser!"
echo "If not, run: open output/opportunities_dashboard.html"
echo ""
