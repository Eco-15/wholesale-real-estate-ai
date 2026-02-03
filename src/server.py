"""
WHOLESALE OPPORTUNITIES WEB SERVER
===================================

Live web server that automatically serves the latest dashboard data.

Usage:
    python3 server.py

Then visit: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify
import pandas as pd
from pathlib import Path
import json

app = Flask(__name__)

def load_data():
    """Load the latest opportunities and properties data"""
    opportunities_path = 'data/real_estate_data_opportunities.csv'
    all_properties_path = 'data/real_estate_data.csv'

    # Load opportunities
    opportunities = []
    if Path(opportunities_path).exists():
        opportunities = pd.read_csv(opportunities_path).to_dict('records')

    # Load all properties
    all_properties = []
    all_props_stats = {
        'total': 0,
        'avg_listed_price': 0,
        'avg_market_value': 0,
        'avg_sqft': 0,
        'avg_days_on_market': 0,
        'foreclosure_count': 0,
    }

    if Path(all_properties_path).exists():
        df = pd.read_csv(all_properties_path)
        all_properties = df.to_dict('records')
        all_props_stats = {
            'total': len(df),
            'avg_listed_price': float(df['listed_price'].mean()),
            'avg_market_value': float(df['true_market_value'].mean()) if 'true_market_value' in df.columns else 0,
            'avg_sqft': float(df['square_feet'].mean()),
            'avg_days_on_market': float(df['days_on_market'].mean()),
            'foreclosure_count': int(df['is_foreclosure'].sum()) if 'is_foreclosure' in df.columns else 0,
        }

    # Calculate stats
    if opportunities:
        df_opp = pd.DataFrame(opportunities)
        stats = {
            'total_opportunities': len(df_opp),
            'total_properties': all_props_stats['total'],
            'avg_spread': float(df_opp['predicted_spread'].mean()),
            'avg_profit': float(df_opp['estimated_profit'].mean()),
            'avg_score': float(df_opp['opportunity_score'].mean()),
            'total_potential_profit': float(df_opp['estimated_profit'].sum()),
            'avg_days_on_market': float(df_opp['days_on_market'].mean()),
            'foreclosure_count': int(df_opp['is_foreclosure'].sum()) if 'is_foreclosure' in df_opp.columns else 0,
        }
    else:
        stats = {
            'total_opportunities': 0,
            'total_properties': 0,
            'avg_spread': 0,
            'avg_profit': 0,
            'avg_score': 0,
            'total_potential_profit': 0,
            'avg_days_on_market': 0,
            'foreclosure_count': 0,
        }

    return {
        'opportunities': opportunities,
        'all_properties': all_properties,
        'stats': stats,
        'all_props_stats': all_props_stats
    }

@app.route('/')
def index():
    """Main dashboard page"""
    data = load_data()

    # Ensure output directory exists
    Path('output').mkdir(exist_ok=True)

    # Read the HTML template from view_opportunities.py
    from view_opportunities import generate_dashboard

    # Generate fresh HTML with current data
    generate_dashboard()

    # Read and serve the generated HTML
    with open('output/opportunities_dashboard.html', 'r') as f:
        html_content = f.read()

    return html_content

@app.route('/api/data')
def api_data():
    """API endpoint to get fresh data (for live updates)"""
    return jsonify(load_data())

@app.route('/api/refresh')
def api_refresh():
    """API endpoint to trigger full data refresh"""
    import subprocess
    try:
        # Run the refresh script
        subprocess.run(['./scripts/refresh_data.sh'], check=True)
        return jsonify({'success': True, 'message': 'Dashboard refreshed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print("\n" + "="*60)
    print("🚀 WHOLESALE OPPORTUNITIES WEB SERVER")
    print("="*60)
    print("\n📊 Dashboard is now running!")
    print(f"\n🌐 Open in your browser:")
    print(f"   http://localhost:{port}")
    print("\n📡 API Endpoints:")
    print(f"   http://localhost:{port}/api/data - Get fresh data")
    print(f"   http://localhost:{port}/api/refresh - Regenerate all data")
    print("\n💡 The server will automatically show the latest data")
    print("   Just refresh your browser after running refresh_data.sh")
    print("\n⌨️  Press Ctrl+C to stop the server")
    print("="*60 + "\n")

    app.run(debug=debug, host='0.0.0.0', port=port)
