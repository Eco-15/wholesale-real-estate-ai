"""
HOW TO USE THIS WHOLESALE FINDER WITH YOUR OWN DATA
=====================================================

Once you get real data from PropStream, MLS, or scraping, here's how to use it:

1. Export your data to CSV with these columns (minimum required):
   - neighborhood (or location/city)
   - property_type (Single Family, Condo, etc.)
   - bedrooms
   - bathrooms
   - square_feet
   - lot_size
   - year_built
   - condition (Excellent, Good, Fair, Poor, Distressed)
   - days_on_market
   - price_reductions
   - is_foreclosure (0 or 1)
   - has_lien (0 or 1)
   - owner_occupied (0 or 1)
   - num_distress_keywords (count of keywords like "motivated", "as-is", etc.)
   - listed_price
   - estimated_repair_cost (your estimate or use default)

2. Run this script with your CSV file
3. Get ranked wholesale opportunities!

"""

import pandas as pd
import sys
from wholesale_model import RealEstateWholesaleModel

def analyze_new_properties(csv_path, min_spread=20000, min_spread_pct=10):
    """
    Analyze new properties and find wholesale opportunities
    
    Args:
        csv_path: Path to CSV file with property data
        min_spread: Minimum dollar spread to consider (default $20k)
        min_spread_pct: Minimum spread percentage (default 10%)
    """
    
    print("=" * 80)
    print("🏠 ANALYZING NEW PROPERTIES FOR WHOLESALE OPPORTUNITIES")
    print("=" * 80)
    
    # Load the trained model
    print("\n📂 Loading trained model...")
    model = RealEstateWholesaleModel()
    model.load_model('models/wholesale_model.pkl')
    
    # Load new data
    print(f"\n📁 Loading properties from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} properties")
    
    # Calculate age if not present
    if 'age' not in df.columns and 'year_built' in df.columns:
        df['age'] = 2024 - df['year_built']
    
    # Set defaults for missing columns
    if 'estimated_repair_cost' not in df.columns:
        print("⚠️  No repair costs provided, using estimates based on condition")
        df['estimated_repair_cost'] = df['condition'].map({
            'Excellent': 2000,
            'Good': 5000,
            'Fair': 15000,
            'Poor': 30000,
            'Distressed': 40000
        })
    
    if 'is_foreclosure' not in df.columns:
        df['is_foreclosure'] = 0
    if 'has_lien' not in df.columns:
        df['has_lien'] = 0
    if 'owner_occupied' not in df.columns:
        df['owner_occupied'] = 1
    if 'num_distress_keywords' not in df.columns:
        df['num_distress_keywords'] = 0
    
    # Find opportunities
    opportunities, all_results = model.find_opportunities(
        df,
        min_spread=min_spread,
        min_spread_pct=min_spread_pct
    )
    
    # Display results
    if len(opportunities) == 0:
        print("\n❌ No wholesale opportunities found with current criteria.")
        print(f"   Try lowering min_spread (currently ${min_spread:,})")
        print(f"   or min_spread_pct (currently {min_spread_pct}%)")
        return None, None
    
    print("\n" + "=" * 80)
    print(f"💰 TOP 10 WHOLESALE OPPORTUNITIES")
    print("=" * 80)
    
    for idx, (_, row) in enumerate(opportunities.head(10).iterrows(), 1):
        print(f"\n🎯 #{idx} - Score: {row['opportunity_score']:.1f}")
        
        # Show property ID if available
        if 'property_id' in row:
            print(f"   ID: {row['property_id']}")
        if 'address' in row:
            print(f"   📍 {row['address']}")
        else:
            print(f"   📍 {row['neighborhood']} - {row['property_type']}")
        
        print(f"   🏡 {row['bedrooms']} bed, {row['bathrooms']} bath, {row['square_feet']:,} sqft")
        print(f"   🔧 Condition: {row['condition']}")
        print(f"   📅 Days on Market: {row['days_on_market']} | Price Drops: {row['price_reductions']}")
        print(f"   💵 Listed: ${row['listed_price']:,}")
        print(f"   📊 Predicted Market Value: ${row['predicted_market_value']:,}")
        print(f"   💰 Spread: ${row['predicted_spread']:,} ({row['predicted_spread_pct']:.1f}%)")
        print(f"   🔨 Repair Cost: ${row['estimated_repair_cost']:,}")
        print(f"   ✅ Est. Profit: ${row['estimated_profit']:,}")
        print(f"   🚨 Distress Score: {row['distress_score']:.1f}")
    
    # Save results
    output_file = csv_path.replace('.csv', '_opportunities.csv')
    opportunities.to_csv(output_file, index=False)
    
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Total opportunities: {len(opportunities)}")
    print(f"💰 Avg spread: ${opportunities['predicted_spread'].mean():,.0f}")
    print(f"💰 Avg profit: ${opportunities['estimated_profit'].mean():,.0f}")
    print(f"\n📁 Results saved to: {output_file}")
    print("=" * 80)
    
    return opportunities, all_results


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        # Use provided CSV file
        csv_path = sys.argv[1]
        analyze_new_properties(csv_path)
    else:
        # Demo with the synthetic data
        print("DEMO MODE - Using synthetic test data")
        print("To analyze your own data, run:")
        print("  python use_model.py your_properties.csv")
        print()

        analyze_new_properties('data/real_estate_data.csv')
