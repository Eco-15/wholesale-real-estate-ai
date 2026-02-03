"""
WHOLESALE OPPORTUNITIES VIEWER - SLEEK BLACK & WHITE EDITION
============================================================

This script generates a minimalist black and white dashboard.

Usage:
    python3 view_opportunities_bw.py
    python3 view_opportunities_bw.py custom_opportunities.csv
"""

import pandas as pd
import json
import sys
from pathlib import Path

def generate_dashboard(csv_path='data/real_estate_data_opportunities.csv', all_properties_path='data/real_estate_data.csv'):
    """
    Generate a sleek black & white HTML dashboard
    """

    print(f"\nGenerating dashboard...")
    print(f"Loading data from: {csv_path}")

    # Load opportunity data
    if not Path(csv_path).exists():
        print(f"Error: {csv_path} not found!")
        print("Run 'python3 use_model.py' first to generate opportunities.")
        return

    opportunities = pd.read_csv(csv_path)

    # Load all properties if available
    all_properties = None
    all_properties_json = "[]"
    all_props_stats = {}

    if Path(all_properties_path).exists():
        all_properties = pd.read_csv(all_properties_path)
        print(f"Loaded {len(all_properties)} total properties")
        all_properties_json = all_properties.to_json(orient='records')

        # Calculate spread and profit if true_market_value exists
        avg_spread = 0
        avg_profit = 0
        total_potential = 0
        if 'true_market_value' in all_properties.columns:
            all_properties['spread'] = all_properties['true_market_value'] - all_properties['listed_price']
            # Simple profit estimate: spread minus 15% for repairs
            all_properties['profit_estimate'] = all_properties['spread'] * 0.85
            avg_spread = float(all_properties['spread'].mean())
            avg_profit = float(all_properties['profit_estimate'].mean())
            total_potential = float(all_properties['profit_estimate'].sum())

        all_props_stats = {
            'total': len(all_properties),
            'avg_listed_price': float(all_properties['listed_price'].mean()),
            'avg_market_value': float(all_properties['true_market_value'].mean()) if 'true_market_value' in all_properties.columns else 0,
            'avg_sqft': float(all_properties['square_feet'].mean()),
            'avg_spread': avg_spread,
            'avg_profit': avg_profit,
            'total_potential': total_potential,
            'avg_days_on_market': float(all_properties['days_on_market'].mean()),
            'avg_opportunity_score': float(all_properties['opportunity_score'].mean()) if 'opportunity_score' in all_properties.columns else 0,
            'avg_distress_score': float(all_properties['distress_score'].mean()) if 'distress_score' in all_properties.columns else 0,
            'foreclosure_count': int(all_properties['is_foreclosure'].sum()) if 'is_foreclosure' in all_properties.columns else 0,
        }
    else:
        print("Warning: All properties data not found")

    print(f"Loaded {len(opportunities)} wholesale opportunities")

    # Calculate statistics
    stats = {
        'total_opportunities': len(opportunities),
        'total_properties': len(all_properties) if all_properties is not None else len(opportunities),
        'avg_listed_price': float(opportunities['listed_price'].mean()),
        'avg_sqft': float(opportunities['square_feet'].mean()),
        'avg_spread': float(opportunities['predicted_spread'].mean()),
        'avg_profit': float(opportunities['estimated_profit'].mean()),
        'avg_score': float(opportunities['opportunity_score'].mean()),
        'avg_distress_score': float(opportunities['distress_score'].mean()) if 'distress_score' in opportunities.columns else 0,
        'total_potential_profit': float(opportunities['estimated_profit'].sum()),
        'avg_days_on_market': float(opportunities['days_on_market'].mean()),
        'foreclosure_count': int(opportunities['is_foreclosure'].sum()) if 'is_foreclosure' in opportunities.columns else 0,
    }

    # Convert to JSON
    opportunities_json = opportunities.to_json(orient='records')

    # Generate sleek black & white HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wholesale Opportunities</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #ffffff;
            min-height: 100vh;
            padding: 40px 20px;
            color: #000000;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 30px;
            margin-bottom: 40px;
        }}

        .header h1 {{
            font-size: 2.5em;
            font-weight: 300;
            letter-spacing: -0.02em;
            color: #000000;
            margin-bottom: 10px;
        }}

        .header p {{
            color: #666;
            font-size: 1em;
            font-weight: 300;
        }}

        /* Tabs */
        .tabs {{
            border-bottom: 1px solid #ddd;
            margin-bottom: 40px;
        }}

        .tab-buttons {{
            display: flex;
            gap: 40px;
        }}

        .tab-button {{
            background: none;
            border: none;
            color: #999;
            padding: 15px 0;
            cursor: pointer;
            font-size: 0.95em;
            font-weight: 400;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            transition: all 0.2s;
            position: relative;
        }}

        .tab-button:hover {{
            color: #555;
        }}

        .tab-button.active {{
            color: #000000;
        }}

        .tab-button.active::after {{
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 1px;
            background: #000000;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1px;
            background: #ddd;
            border: 1px solid #ddd;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: #fff;
            padding: 30px;
            transition: background 0.2s;
        }}

        .stat-card:hover {{
            background: #f5f5f5;
        }}

        .stat-card .label {{
            color: #999;
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
            font-weight: 400;
        }}

        .stat-card .value {{
            color: #000000;
            font-size: 2.2em;
            font-weight: 300;
            letter-spacing: -0.02em;
        }}

        .stat-card .subtext {{
            color: #aaa;
            font-size: 0.85em;
            margin-top: 8px;
            font-weight: 300;
        }}

        /* Controls */
        .controls {{
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 30px;
            margin-bottom: 40px;
        }}

        .controls-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .controls-row:last-child {{
            margin-bottom: 0;
        }}

        .control-group label {{
            display: block;
            color: #999;
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 8px;
            font-weight: 400;
        }}

        .control-group input,
        .control-group select {{
            width: 100%;
            padding: 12px;
            background: #fff;
            border: 1px solid #ccc;
            color: #000;
            font-size: 0.95em;
            transition: border-color 0.2s;
        }}

        .control-group input:focus,
        .control-group select:focus {{
            outline: none;
            border-color: #999;
        }}

        .btn {{
            background: #000000;
            color: #fff;
            padding: 12px 24px;
            border: none;
            cursor: pointer;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.2s;
            font-weight: 500;
        }}

        .btn:hover {{
            background: #222;
        }}

        .btn-secondary {{
            background: #ddd;
            color: #000;
        }}

        .btn-secondary:hover {{
            background: #ccc;
        }}

        #refresh-btn:hover {{
            background: #222;
        }}

        #refresh-btn:disabled {{
            cursor: not-allowed;
            opacity: 0.6;
        }}

        /* Properties Container */
        .properties-container {{
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 30px;
        }}

        .properties-header {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }}

        .properties-header h2 {{
            font-size: 1.2em;
            font-weight: 300;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #777;
        }}

        /* Property Cards */
        .property-card {{
            border: 1px solid #ddd;
            padding: 25px;
            margin-bottom: 1px;
            transition: all 0.2s;
            cursor: pointer;
            background: #fff;
        }}

        .property-card:hover {{
            border-color: #bbb;
            background: #f0f0f0;
        }}

        .property-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e5e5;
        }}

        .property-rank {{
            background: #000000;
            color: #fff;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 500;
            font-size: 0.9em;
            letter-spacing: 0.02em;
        }}

        .property-score {{
            background: #e5e5e5;
            padding: 6px 14px;
            font-size: 0.85em;
            color: #000;
            font-weight: 400;
            letter-spacing: 0.05em;
        }}

        .property-id {{
            font-size: 1.1em;
            font-weight: 400;
            color: #000000;
            margin-bottom: 8px;
            letter-spacing: 0.02em;
        }}

        .property-location {{
            color: #999;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}

        .property-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 20px;
        }}

        .detail-item {{
            display: flex;
            flex-direction: column;
        }}

        .detail-label {{
            color: #aaa;
            font-size: 0.7em;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 6px;
        }}

        .detail-value {{
            color: #000000;
            font-weight: 400;
            font-size: 1em;
        }}

        .detail-value.highlight {{
            color: #000000;
            font-weight: 500;
        }}

        .property-tags {{
            display: flex;
            gap: 8px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .tag {{
            padding: 4px 10px;
            font-size: 0.75em;
            font-weight: 400;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            border: 1px solid #ccc;
            color: #777;
        }}

        .tag.condition-excellent {{ border-color: #bbb; color: #666; }}
        .tag.condition-good {{ border-color: #bbb; color: #666; }}
        .tag.condition-fair {{ border-color: #aaa; color: #555; }}
        .tag.condition-poor {{ border-color: #999; color: #444; }}
        .tag.condition-distressed {{ border-color: #888; color: #333; }}
        .tag.foreclosure {{ border-color: #777; color: #222; }}
        .tag.high-distress {{ border-color: #666; color: #111; }}

        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1000;
            overflow-y: auto;
            padding: 40px 20px;
        }}

        .modal.active {{
            display: flex;
            align-items: flex-start;
            justify-content: center;
        }}

        .modal-content {{
            background: #f5f5f5;
            border: 1px solid #ddd;
            max-width: 900px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
        }}

        .modal-header {{
            background: #fff;
            border-bottom: 1px solid #ddd;
            padding: 30px;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        .modal-header h2 {{
            color: #000000;
            font-size: 1.8em;
            font-weight: 300;
            margin-bottom: 8px;
            letter-spacing: -0.01em;
        }}

        .modal-header p {{
            color: #999;
            font-size: 0.95em;
        }}

        .modal-close {{
            position: absolute;
            top: 30px;
            right: 30px;
            background: none;
            border: 1px solid #ccc;
            color: #000;
            font-size: 1.2em;
            width: 36px;
            height: 36px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .modal-close:hover {{
            border-color: #999;
            background: #eee;
        }}

        .modal-body {{
            padding: 30px;
        }}

        .modal-section {{
            margin-bottom: 40px;
        }}

        .modal-section:last-child {{
            margin-bottom: 0;
        }}

        .modal-section h3 {{
            color: #777;
            margin-bottom: 20px;
            font-size: 0.85em;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            border-bottom: 1px solid #ddd;
            padding-bottom: 12px;
        }}

        .modal-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1px;
            background: #ddd;
            border: 1px solid #ddd;
        }}

        .modal-detail {{
            background: #fff;
            padding: 20px;
        }}

        .modal-detail-label {{
            color: #aaa;
            font-size: 0.7em;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 8px;
        }}

        .modal-detail-value {{
            color: #000000;
            font-size: 1.3em;
            font-weight: 300;
            letter-spacing: -0.01em;
        }}

        .profit-breakdown {{
            background: #000000;
            color: #fff;
            padding: 30px;
            margin-top: 20px;
        }}

        .profit-breakdown h4 {{
            margin-bottom: 20px;
            font-size: 0.85em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .profit-item {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #222;
            font-size: 0.95em;
        }}

        .profit-item:last-child {{
            border-bottom: none;
            border-top: 2px solid #fff;
            font-size: 1.2em;
            font-weight: 500;
            margin-top: 10px;
            padding-top: 20px;
        }}

        .no-results {{
            text-align: center;
            padding: 80px 20px;
            color: #aaa;
        }}

        .no-results h3 {{
            font-size: 1.2em;
            font-weight: 300;
            margin-bottom: 10px;
            letter-spacing: 0.05em;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 20px 15px;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .controls-row {{
                grid-template-columns: 1fr;
            }}

            .property-details {{
                grid-template-columns: 1fr;
            }}

            .tab-buttons {{
                gap: 20px;
            }}

            .tab-button {{
                font-size: 0.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1>Wholesale Opportunities</h1>
                    <p>Real Estate Investment Analysis Platform</p>
                </div>
                <button id="refresh-btn" onclick="refreshData()" style="
                    background: #000000;
                    color: #fff;
                    border: none;
                    padding: 12px 24px;
                    cursor: pointer;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    transition: all 0.2s;
                    font-weight: 500;
                ">
                    Refresh Data
                </button>
            </div>
            <div id="refresh-status" style="margin-top: 15px; font-size: 0.9em; color: #888; font-weight: 300;"></div>
        </div>

        <div class="tabs">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="switchTab('opportunities')">
                    Best Opportunities ({stats['total_opportunities']})
                </button>
                <button class="tab-button" onclick="switchTab('all-properties')">
                    All Properties ({stats['total_properties']})
                </button>
            </div>
        </div>

        <div id="opportunities-tab" class="tab-content active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="label">Total Opportunities</div>
                    <div class="value" id="stat-total-opps">{stats['total_opportunities']}</div>
                    <div class="subtext" id="stat-total-opps-subtext">out of {stats['total_properties']} properties</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Listed Price</div>
                    <div class="value" id="stat-avg-listed-price">${stats['avg_listed_price']:,.0f}</div>
                    <div class="subtext">Average asking price</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Square Feet</div>
                    <div class="value" id="stat-avg-sqft">{stats['avg_sqft']:,.0f}</div>
                    <div class="subtext">Average property size</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Spread</div>
                    <div class="value" id="stat-avg-spread">${stats['avg_spread']:,.0f}</div>
                    <div class="subtext">Average profit potential</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Profit</div>
                    <div class="value" id="stat-avg-profit">${stats['avg_profit']:,.0f}</div>
                    <div class="subtext">After estimated repairs</div>
                </div>
                <div class="stat-card">
                    <div class="label">Foreclosures</div>
                    <div class="value" id="stat-foreclosures">{stats['foreclosure_count']}</div>
                    <div class="subtext">Properties in foreclosure</div>
                </div>
                <div class="stat-card">
                    <div class="label">Total Potential</div>
                    <div class="value" id="stat-total-potential">${stats['total_potential_profit']:,.0f}</div>
                    <div class="subtext">Combined profit potential</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Opportunity Score</div>
                    <div class="value" id="stat-avg-opp-score">{stats['avg_score']:.1f}</div>
                    <div class="subtext">Investment attractiveness</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Distress Score</div>
                    <div class="value" id="stat-avg-distress">{stats['avg_distress_score']:.1f}</div>
                    <div class="subtext">Property distress level</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Days on Market</div>
                    <div class="value" id="stat-avg-days">{stats['avg_days_on_market']:.0f}</div>
                    <div class="subtext">Time listed</div>
                </div>
            </div>

            <div class="controls">
                <div class="controls-row">
                    <div class="control-group">
                        <label>Search</label>
                        <input type="text" id="searchInput" placeholder="Property ID, neighborhood">
                    </div>
                    <div class="control-group">
                        <label>Condition</label>
                        <select id="conditionFilter">
                            <option value="">All Conditions</option>
                            <option value="Excellent">Excellent</option>
                            <option value="Good">Good</option>
                            <option value="Fair">Fair</option>
                            <option value="Poor">Poor</option>
                            <option value="Distressed">Distressed</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label>Property Type</label>
                        <select id="typeFilter">
                            <option value="">All Types</option>
                            <option value="Single Family">Single Family</option>
                            <option value="Condo">Condo</option>
                            <option value="Townhouse">Townhouse</option>
                            <option value="Multi-Family">Multi-Family</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label>Min Profit</label>
                        <input type="number" id="minProfit" placeholder="50000" step="1000">
                    </div>
                </div>
                <div class="controls-row">
                    <div class="control-group">
                        <label>Sort By</label>
                        <select id="sortBy">
                            <option value="opportunity_score">Opportunity Score</option>
                            <option value="estimated_profit">Estimated Profit</option>
                            <option value="predicted_spread">Predicted Spread</option>
                            <option value="predicted_spread_pct">Spread Percentage</option>
                            <option value="distress_score">Distress Score</option>
                            <option value="days_on_market">Days on Market</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label>&nbsp;</label>
                        <button class="btn" onclick="applyFilters()">Apply Filters</button>
                    </div>
                    <div class="control-group">
                        <label>&nbsp;</label>
                        <button class="btn btn-secondary" onclick="resetFilters()">Reset</button>
                    </div>
                </div>
            </div>

            <div class="properties-container">
                <div class="properties-header">
                    <h2>Opportunities (<span id="resultCount">0</span>)</h2>
                </div>
                <div id="propertiesList"></div>
            </div>
        </div>

        <div id="all-properties-tab" class="tab-content">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="label">Total Properties</div>
                    <div class="value" id="stat-total-props-all">{all_props_stats.get('total', 0)}</div>
                    <div class="subtext">Complete dataset</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Listed Price</div>
                    <div class="value" id="stat-avg-listed-price-all">${all_props_stats.get('avg_listed_price', 0):,.0f}</div>
                    <div class="subtext">Average asking price</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Square Feet</div>
                    <div class="value" id="stat-avg-sqft-all">{all_props_stats.get('avg_sqft', 0):,.0f}</div>
                    <div class="subtext">Average property size</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Spread</div>
                    <div class="value" id="stat-avg-spread-all">${all_props_stats.get('avg_spread', 0):,.0f}</div>
                    <div class="subtext">Average profit potential</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Profit</div>
                    <div class="value" id="stat-avg-profit-all">${all_props_stats.get('avg_profit', 0):,.0f}</div>
                    <div class="subtext">After estimated repairs</div>
                </div>
                <div class="stat-card">
                    <div class="label">Foreclosures</div>
                    <div class="value" id="stat-foreclosures-all">{all_props_stats.get('foreclosure_count', 0)}</div>
                    <div class="subtext">Properties in foreclosure</div>
                </div>
                <div class="stat-card">
                    <div class="label">Total Potential</div>
                    <div class="value" id="stat-total-potential-all">${all_props_stats.get('total_potential', 0):,.0f}</div>
                    <div class="subtext">Combined profit potential</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Opportunity Score</div>
                    <div class="value" id="stat-avg-opp-score-all">{all_props_stats.get('avg_opportunity_score', 0):.1f}</div>
                    <div class="subtext">Investment attractiveness</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Distress Score</div>
                    <div class="value" id="stat-avg-distress-all">{all_props_stats.get('avg_distress_score', 0):.1f}</div>
                    <div class="subtext">Property distress level</div>
                </div>
                <div class="stat-card">
                    <div class="label">Avg Days on Market</div>
                    <div class="value" id="stat-avg-days-all">{all_props_stats.get('avg_days_on_market', 0):.0f}</div>
                    <div class="subtext">Time listed</div>
                </div>
            </div>

            <div class="controls">
                <div class="controls-row">
                    <div class="control-group">
                        <label>Search</label>
                        <input type="text" id="searchInputAll" placeholder="Property ID, neighborhood">
                    </div>
                    <div class="control-group">
                        <label>Condition</label>
                        <select id="conditionFilterAll">
                            <option value="">All Conditions</option>
                            <option value="Excellent">Excellent</option>
                            <option value="Good">Good</option>
                            <option value="Fair">Fair</option>
                            <option value="Poor">Poor</option>
                            <option value="Distressed">Distressed</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label>Property Type</label>
                        <select id="typeFilterAll">
                            <option value="">All Types</option>
                            <option value="Single Family">Single Family</option>
                            <option value="Condo">Condo</option>
                            <option value="Townhouse">Townhouse</option>
                            <option value="Multi-Family">Multi-Family</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label>Max Price</label>
                        <input type="number" id="maxPrice" placeholder="500000" step="10000">
                    </div>
                </div>
                <div class="controls-row">
                    <div class="control-group">
                        <label>Sort By</label>
                        <select id="sortByAll">
                            <option value="listed_price">Listed Price</option>
                            <option value="square_feet">Square Feet</option>
                            <option value="days_on_market">Days on Market</option>
                            <option value="price_reductions">Price Reductions</option>
                            <option value="year_built">Year Built</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label>&nbsp;</label>
                        <button class="btn" onclick="applyFiltersAll()">Apply Filters</button>
                    </div>
                    <div class="control-group">
                        <label>&nbsp;</label>
                        <button class="btn btn-secondary" onclick="resetFiltersAll()">Reset</button>
                    </div>
                </div>
            </div>

            <div class="properties-container">
                <div class="properties-header">
                    <h2>All Properties (<span id="resultCountAll">0</span>)</h2>
                </div>
                <div id="propertiesListAll"></div>
            </div>
        </div>
    </div>

    <div class="modal" id="propertyModal">
        <div class="modal-content">
            <div class="modal-header">
                <button class="modal-close" onclick="closeModal()">×</button>
                <h2 id="modalTitle">Property Details</h2>
                <p id="modalSubtitle"></p>
            </div>
            <div class="modal-body" id="modalBody"></div>
        </div>
    </div>

    <script>
        const opportunitiesData = {opportunities_json};
        const allPropertiesData = {all_properties_json};
        let filteredProperties = [...opportunitiesData];
        let filteredAllProperties = [...allPropertiesData];
        let currentTab = 'opportunities';

        document.addEventListener('DOMContentLoaded', function() {{
            applyFilters();
            applyFiltersAll();

            document.getElementById('searchInput').addEventListener('keyup', function(e) {{
                if (e.key === 'Enter') applyFilters();
            }});
            document.getElementById('searchInputAll').addEventListener('keyup', function(e) {{
                if (e.key === 'Enter') applyFiltersAll();
            }});
        }});

        function switchTab(tab) {{
            currentTab = tab;
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            if (tab === 'opportunities') {{
                document.getElementById('opportunities-tab').classList.add('active');
            }} else {{
                document.getElementById('all-properties-tab').classList.add('active');
            }}
        }}

        function updateOpportunitiesStats() {{
            const total = filteredProperties.length;
            const avgListedPrice = total > 0 ? filteredProperties.reduce((sum, p) => sum + p.listed_price, 0) / total : 0;
            const avgSqft = total > 0 ? filteredProperties.reduce((sum, p) => sum + p.square_feet, 0) / total : 0;
            const avgSpread = total > 0 ? filteredProperties.reduce((sum, p) => sum + p.predicted_spread, 0) / total : 0;
            const avgProfit = total > 0 ? filteredProperties.reduce((sum, p) => sum + p.estimated_profit, 0) / total : 0;
            const totalPotential = filteredProperties.reduce((sum, p) => sum + p.estimated_profit, 0);
            const avgOppScore = total > 0 ? filteredProperties.reduce((sum, p) => sum + p.opportunity_score, 0) / total : 0;
            const avgDistress = total > 0 ? filteredProperties.reduce((sum, p) => sum + p.distress_score, 0) / total : 0;
            const avgDays = total > 0 ? filteredProperties.reduce((sum, p) => sum + p.days_on_market, 0) / total : 0;
            const foreclosures = filteredProperties.filter(p => p.is_foreclosure).length;

            document.getElementById('stat-total-opps').textContent = total;
            document.getElementById('stat-total-opps-subtext').textContent = `out of ${{opportunitiesData.length}} properties`;
            document.getElementById('stat-avg-listed-price').textContent = `$${{Math.round(avgListedPrice).toLocaleString()}}`;
            document.getElementById('stat-avg-sqft').textContent = Math.round(avgSqft).toLocaleString();
            document.getElementById('stat-avg-spread').textContent = `$${{Math.round(avgSpread).toLocaleString()}}`;
            document.getElementById('stat-avg-profit').textContent = `$${{Math.round(avgProfit).toLocaleString()}}`;
            document.getElementById('stat-total-potential').textContent = `$${{Math.round(totalPotential).toLocaleString()}}`;
            document.getElementById('stat-avg-opp-score').textContent = avgOppScore.toFixed(1);
            document.getElementById('stat-avg-distress').textContent = avgDistress.toFixed(1);
            document.getElementById('stat-avg-days').textContent = Math.round(avgDays);
            document.getElementById('stat-foreclosures').textContent = foreclosures;
        }}

        function applyFilters() {{
            const search = document.getElementById('searchInput').value.toLowerCase();
            const condition = document.getElementById('conditionFilter').value;
            const type = document.getElementById('typeFilter').value;
            const minProfit = parseFloat(document.getElementById('minProfit').value) || 0;
            const sortBy = document.getElementById('sortBy').value;

            filteredProperties = opportunitiesData.filter(prop => {{
                const matchesSearch = !search ||
                    (prop.property_id && prop.property_id.toLowerCase().includes(search)) ||
                    (prop.neighborhood && prop.neighborhood.toLowerCase().includes(search)) ||
                    (prop.address && prop.address.toLowerCase().includes(search));

                const matchesCondition = !condition || prop.condition === condition;
                const matchesType = !type || prop.property_type === type;
                const matchesProfit = prop.estimated_profit >= minProfit;

                return matchesSearch && matchesCondition && matchesType && matchesProfit;
            }});

            filteredProperties.sort((a, b) => b[sortBy] - a[sortBy]);
            updateOpportunitiesStats();
            renderProperties();
        }}

        function resetFilters() {{
            document.getElementById('searchInput').value = '';
            document.getElementById('conditionFilter').value = '';
            document.getElementById('typeFilter').value = '';
            document.getElementById('minProfit').value = '';
            document.getElementById('sortBy').value = 'opportunity_score';
            applyFilters();
        }}

        function renderProperties() {{
            const container = document.getElementById('propertiesList');
            const countEl = document.getElementById('resultCount');
            countEl.textContent = filteredProperties.length;

            if (filteredProperties.length === 0) {{
                container.innerHTML = '<div class="no-results"><h3>No properties found</h3><p>Try adjusting your filters</p></div>';
                return;
            }}

            container.innerHTML = filteredProperties.map((prop, index) => `
                <div class="property-card" onclick="showPropertyDetail(${{index}}, 'opportunities')">
                    <div class="property-card-header">
                        <div class="property-rank">${{index + 1}}</div>
                        <div class="property-score">Score: ${{prop.opportunity_score.toFixed(1)}}</div>
                    </div>
                    <div class="property-id">${{prop.property_id || 'N/A'}}</div>
                    <div class="property-location">${{prop.neighborhood}} - ${{prop.property_type}}</div>
                    <div class="property-details">
                        <div class="detail-item">
                            <div class="detail-label">Listed Price</div>
                            <div class="detail-value">$${{prop.listed_price.toLocaleString()}}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Market Value</div>
                            <div class="detail-value">$${{prop.predicted_market_value.toLocaleString()}}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Spread</div>
                            <div class="detail-value highlight">$${{prop.predicted_spread.toLocaleString()}}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Est. Profit</div>
                            <div class="detail-value highlight">$${{prop.estimated_profit.toLocaleString()}}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Size</div>
                            <div class="detail-value">${{prop.bedrooms}} bed / ${{prop.bathrooms}} bath</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Square Feet</div>
                            <div class="detail-value">${{prop.square_feet.toLocaleString()}} sqft</div>
                        </div>
                    </div>
                    <div class="property-tags">
                        <span class="tag condition-${{prop.condition.toLowerCase()}}">${{prop.condition}}</span>
                        ${{prop.is_foreclosure ? '<span class="tag foreclosure">Foreclosure</span>' : ''}}
                        ${{prop.distress_score > 50 ? '<span class="tag high-distress">High Distress</span>' : ''}}
                        <span class="tag">${{prop.days_on_market}} days on market</span>
                        ${{prop.price_reductions > 0 ? `<span class="tag">${{prop.price_reductions}} price cuts</span>` : ''}}
                    </div>
                </div>
            `).join('');
        }}

        function updateAllPropertiesStats() {{
            const total = filteredAllProperties.length;
            const avgListedPrice = total > 0 ? filteredAllProperties.reduce((sum, p) => sum + p.listed_price, 0) / total : 0;
            const avgSqft = total > 0 ? filteredAllProperties.reduce((sum, p) => sum + p.square_feet, 0) / total : 0;

            // Calculate spread and profit if true_market_value exists
            let avgSpread = 0;
            let avgProfit = 0;
            let totalPotential = 0;
            if (total > 0 && filteredAllProperties[0].true_market_value !== undefined) {{
                const spreads = filteredAllProperties.map(p => p.true_market_value - p.listed_price);
                const profits = spreads.map(s => s * 0.85);
                avgSpread = spreads.reduce((sum, s) => sum + s, 0) / total;
                avgProfit = profits.reduce((sum, p) => sum + p, 0) / total;
                totalPotential = profits.reduce((sum, p) => sum + p, 0);
            }}

            const avgOppScore = total > 0 && filteredAllProperties[0].opportunity_score !== undefined
                ? filteredAllProperties.reduce((sum, p) => sum + (p.opportunity_score || 0), 0) / total : 0;
            const avgDistress = total > 0 && filteredAllProperties[0].distress_score !== undefined
                ? filteredAllProperties.reduce((sum, p) => sum + (p.distress_score || 0), 0) / total : 0;
            const avgDays = total > 0 ? filteredAllProperties.reduce((sum, p) => sum + p.days_on_market, 0) / total : 0;
            const foreclosures = filteredAllProperties.filter(p => p.is_foreclosure).length;

            document.getElementById('stat-total-props-all').textContent = total;
            document.getElementById('stat-avg-listed-price-all').textContent = `$${{Math.round(avgListedPrice).toLocaleString()}}`;
            document.getElementById('stat-avg-sqft-all').textContent = Math.round(avgSqft).toLocaleString();
            document.getElementById('stat-avg-spread-all').textContent = `$${{Math.round(avgSpread).toLocaleString()}}`;
            document.getElementById('stat-avg-profit-all').textContent = `$${{Math.round(avgProfit).toLocaleString()}}`;
            document.getElementById('stat-total-potential-all').textContent = `$${{Math.round(totalPotential).toLocaleString()}}`;
            document.getElementById('stat-avg-opp-score-all').textContent = avgOppScore.toFixed(1);
            document.getElementById('stat-avg-distress-all').textContent = avgDistress.toFixed(1);
            document.getElementById('stat-avg-days-all').textContent = Math.round(avgDays);
            document.getElementById('stat-foreclosures-all').textContent = foreclosures;
        }}

        function applyFiltersAll() {{
            const search = document.getElementById('searchInputAll').value.toLowerCase();
            const condition = document.getElementById('conditionFilterAll').value;
            const type = document.getElementById('typeFilterAll').value;
            const maxPrice = parseFloat(document.getElementById('maxPrice').value) || Infinity;
            const sortBy = document.getElementById('sortByAll').value;

            filteredAllProperties = allPropertiesData.filter(prop => {{
                const matchesSearch = !search ||
                    (prop.property_id && prop.property_id.toLowerCase().includes(search)) ||
                    (prop.neighborhood && prop.neighborhood.toLowerCase().includes(search));
                const matchesCondition = !condition || prop.condition === condition;
                const matchesType = !type || prop.property_type === type;
                const matchesPrice = prop.listed_price <= maxPrice;
                return matchesSearch && matchesCondition && matchesType && matchesPrice;
            }});

            filteredAllProperties.sort((a, b) => {{
                if (sortBy === 'year_built') return a[sortBy] - b[sortBy];
                return b[sortBy] - a[sortBy];
            }});

            updateAllPropertiesStats();
            renderAllProperties();
        }}

        function resetFiltersAll() {{
            document.getElementById('searchInputAll').value = '';
            document.getElementById('conditionFilterAll').value = '';
            document.getElementById('typeFilterAll').value = '';
            document.getElementById('maxPrice').value = '';
            document.getElementById('sortByAll').value = 'listed_price';
            applyFiltersAll();
        }}

        function renderAllProperties() {{
            const container = document.getElementById('propertiesListAll');
            const countEl = document.getElementById('resultCountAll');
            countEl.textContent = filteredAllProperties.length;

            if (filteredAllProperties.length === 0) {{
                container.innerHTML = '<div class="no-results"><h3>No properties found</h3><p>Try adjusting your filters</p></div>';
                return;
            }}

            container.innerHTML = filteredAllProperties.map((prop, index) => {{
                const spread = prop.true_market_value ? prop.true_market_value - prop.listed_price : 0;
                return `
                    <div class="property-card" onclick="showPropertyDetail(${{index}}, 'all')">
                        <div class="property-card-header">
                            <div class="property-rank">${{index + 1}}</div>
                        </div>
                        <div class="property-id">${{prop.property_id || 'N/A'}}</div>
                        <div class="property-location">${{prop.neighborhood}} - ${{prop.property_type}}</div>
                        <div class="property-details">
                            <div class="detail-item">
                                <div class="detail-label">Listed Price</div>
                                <div class="detail-value">$${{prop.listed_price.toLocaleString()}}</div>
                            </div>
                            ${{prop.true_market_value ? `
                            <div class="detail-item">
                                <div class="detail-label">True Market Value</div>
                                <div class="detail-value">$${{prop.true_market_value.toLocaleString()}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Spread</div>
                                <div class="detail-value ${{spread > 20000 ? 'highlight' : ''}}">$${{spread.toLocaleString()}}</div>
                            </div>
                            ` : ''}}
                            <div class="detail-item">
                                <div class="detail-label">Size</div>
                                <div class="detail-value">${{prop.bedrooms}} bed / ${{prop.bathrooms}} bath</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Square Feet</div>
                                <div class="detail-value">${{prop.square_feet.toLocaleString()}} sqft</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Year Built</div>
                                <div class="detail-value">${{prop.year_built}}</div>
                            </div>
                        </div>
                        <div class="property-tags">
                            <span class="tag condition-${{prop.condition.toLowerCase()}}">${{prop.condition}}</span>
                            ${{prop.is_foreclosure ? '<span class="tag foreclosure">Foreclosure</span>' : ''}}
                            <span class="tag">${{prop.days_on_market}} days on market</span>
                            ${{prop.price_reductions > 0 ? `<span class="tag">${{prop.price_reductions}} price cuts</span>` : ''}}
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        function showPropertyDetail(index, source) {{
            const prop = source === 'opportunities' ? filteredProperties[index] : filteredAllProperties[index];
            const modal = document.getElementById('propertyModal');
            const modalBody = document.getElementById('modalBody');

            document.getElementById('modalTitle').textContent = prop.property_id || 'Property Details';
            document.getElementById('modalSubtitle').textContent = `${{prop.neighborhood}} - ${{prop.property_type}}`;

            let financialSection = '';
            if (source === 'opportunities') {{
                financialSection = `
                    <div class="modal-section">
                        <h3>Financial Overview</h3>
                        <div class="modal-grid">
                            <div class="modal-detail">
                                <div class="modal-detail-label">Listed Price</div>
                                <div class="modal-detail-value">$${{prop.listed_price.toLocaleString()}}</div>
                            </div>
                            <div class="modal-detail">
                                <div class="modal-detail-label">Predicted Market Value</div>
                                <div class="modal-detail-value">$${{prop.predicted_market_value.toLocaleString()}}</div>
                            </div>
                            <div class="modal-detail">
                                <div class="modal-detail-label">Spread</div>
                                <div class="modal-detail-value">$${{prop.predicted_spread.toLocaleString()}}</div>
                            </div>
                            <div class="modal-detail">
                                <div class="modal-detail-label">Spread %</div>
                                <div class="modal-detail-value">${{prop.predicted_spread_pct.toFixed(1)}}%</div>
                            </div>
                        </div>
                        <div class="profit-breakdown">
                            <h4>Profit Breakdown</h4>
                            <div class="profit-item"><span>Market Value</span><span>$${{prop.predicted_market_value.toLocaleString()}}</span></div>
                            <div class="profit-item"><span>Listed Price</span><span>- $${{prop.listed_price.toLocaleString()}}</span></div>
                            <div class="profit-item"><span>Repair Costs</span><span>- $${{prop.estimated_repair_cost.toLocaleString()}}</span></div>
                            <div class="profit-item"><span>Estimated Profit</span><span>$${{prop.estimated_profit.toLocaleString()}}</span></div>
                        </div>
                    </div>
                `;
            }} else if (prop.true_market_value) {{
                const spread = prop.true_market_value - prop.listed_price;
                financialSection = `
                    <div class="modal-section">
                        <h3>Financial Overview</h3>
                        <div class="modal-grid">
                            <div class="modal-detail">
                                <div class="modal-detail-label">Listed Price</div>
                                <div class="modal-detail-value">$${{prop.listed_price.toLocaleString()}}</div>
                            </div>
                            <div class="modal-detail">
                                <div class="modal-detail-label">True Market Value</div>
                                <div class="modal-detail-value">$${{prop.true_market_value.toLocaleString()}}</div>
                            </div>
                            <div class="modal-detail">
                                <div class="modal-detail-label">Spread</div>
                                <div class="modal-detail-value">$${{spread.toLocaleString()}}</div>
                            </div>
                            <div class="modal-detail">
                                <div class="modal-detail-label">Spread %</div>
                                <div class="modal-detail-value">${{((spread / prop.true_market_value) * 100).toFixed(1)}}%</div>
                            </div>
                        </div>
                    </div>
                `;
            }}

            modalBody.innerHTML = `
                ${{financialSection}}
                <div class="modal-section">
                    <h3>Property Details</h3>
                    <div class="modal-grid">
                        <div class="modal-detail"><div class="modal-detail-label">Bedrooms</div><div class="modal-detail-value">${{prop.bedrooms}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Bathrooms</div><div class="modal-detail-value">${{prop.bathrooms}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Square Feet</div><div class="modal-detail-value">${{prop.square_feet.toLocaleString()}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Lot Size</div><div class="modal-detail-value">${{prop.lot_size.toLocaleString()}} sqft</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Year Built</div><div class="modal-detail-value">${{prop.year_built}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Age</div><div class="modal-detail-value">${{prop.age}} years</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Condition</div><div class="modal-detail-value">${{prop.condition}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Property Type</div><div class="modal-detail-value">${{prop.property_type}}</div></div>
                    </div>
                </div>
                <div class="modal-section">
                    <h3>Property Status</h3>
                    <div class="modal-grid">
                        ${{source === 'opportunities' ? `
                        <div class="modal-detail"><div class="modal-detail-label">Distress Score</div><div class="modal-detail-value">${{prop.distress_score.toFixed(1)}}/100</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Opportunity Score</div><div class="modal-detail-value">${{prop.opportunity_score.toFixed(1)}}/100</div></div>
                        ` : ''}}
                        <div class="modal-detail"><div class="modal-detail-label">Days on Market</div><div class="modal-detail-value">${{prop.days_on_market}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Price Reductions</div><div class="modal-detail-value">${{prop.price_reductions}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Foreclosure</div><div class="modal-detail-value">${{prop.is_foreclosure ? 'Yes' : 'No'}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Has Lien</div><div class="modal-detail-value">${{prop.has_lien ? 'Yes' : 'No'}}</div></div>
                        <div class="modal-detail"><div class="modal-detail-label">Owner Occupied</div><div class="modal-detail-value">${{prop.owner_occupied ? 'Yes' : 'No'}}</div></div>
                    </div>
                </div>
            `;

            modal.classList.add('active');
        }}

        function closeModal() {{
            document.getElementById('propertyModal').classList.remove('active');
        }}

        document.getElementById('propertyModal').addEventListener('click', function(e) {{
            if (e.target === this) closeModal();
        }});

        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeModal();
        }});

        function refreshData() {{
            const btn = document.getElementById('refresh-btn');
            const status = document.getElementById('refresh-status');

            // Disable button and show loading state
            btn.disabled = true;
            btn.style.opacity = '0.6';
            btn.style.cursor = 'not-allowed';
            btn.style.background = '#ccc';
            btn.innerHTML = 'Refreshing...';
            status.textContent = 'Generating new property data and analyzing opportunities...';
            status.style.color = '#666';

            // Call the refresh API endpoint
            fetch('/api/refresh')
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        status.textContent = 'Data refreshed successfully. Reloading page...';
                        status.style.color = '#000';

                        // Reload the page after 1 second to show the new data
                        setTimeout(() => {{
                            window.location.reload();
                        }}, 1000);
                    }} else {{
                        status.textContent = 'Error: ' + (data.error || 'Unknown error');
                        status.style.color = '#000';
                        resetRefreshButton();
                    }}
                }})
                .catch(error => {{
                    status.textContent = 'Error refreshing data: ' + error.message;
                    status.style.color = '#000';
                    resetRefreshButton();
                }});
        }}

        function resetRefreshButton() {{
            const btn = document.getElementById('refresh-btn');
            setTimeout(() => {{
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.style.cursor = 'pointer';
                btn.style.background = '#000000';
                btn.innerHTML = 'Refresh Data';
            }}, 3000);
        }}
    </script>
</body>
</html>"""

    output_file = 'output/opportunities_dashboard.html'
    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"\nDashboard generated successfully!")
    print(f"Saved to: {output_file}")
    print(f"\nTo view: open {output_file}")

    return output_file


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'data/real_estate_data_opportunities.csv'

    if not Path(csv_path).exists():
        opportunities_files = list(Path('.').glob('*_opportunities.csv'))
        if opportunities_files:
            csv_path = str(opportunities_files[0])
            print(f"Found opportunities file: {csv_path}")

    generate_dashboard(csv_path)
