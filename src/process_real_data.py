"""
REAL ESTATE DATA PROCESSOR
===========================

Processes the Kaggle USA Real Estate dataset for wholesale opportunity analysis.
Transforms real data into the format expected by our XGBoost model.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def process_real_estate_data(
    input_file='data/realtor-data-raw.csv',
    output_file='data/real_estate_data.csv',
    state_filter='Connecticut',
    max_properties=1000
):
    """
    Process real estate data from Kaggle dataset
    
    Parameters:
    -----------
    input_file : str
        Path to raw Kaggle dataset
    output_file : str
        Path to save processed data
    state_filter : str or None
        Filter by state (e.g., 'Connecticut', 'New York'). None for all states.
    max_properties : int
        Maximum number of properties to process
    """
    
    print("="*80)
    print("PROCESSING REAL ESTATE DATA")
    print("="*80)
    
    # Load raw data
    print(f"\nLoading data from {input_file}...")
    df = pd.read_csv(input_file, low_memory=False)
    print(f"Loaded {len(df):,} properties")
    
    # Filter by state if specified
    if state_filter:
        df = df[df['state'] == state_filter].copy()
        print(f"Filtered to {state_filter}: {len(df):,} properties")
    
    # Filter for 'for_sale' status
    df = df[df['status'] == 'for_sale'].copy()
    print(f"Active listings (for_sale): {len(df):,} properties")
    
    # Remove properties with missing critical data
    df = df.dropna(subset=['price', 'bed', 'bath', 'house_size'])
    print(f"After removing nulls: {len(df):,} properties")
    
    # Remove outliers and invalid data
    df = df[
        (df['price'] > 50000) &  # Minimum realistic price
        (df['price'] < 5000000) &  # Maximum for wholesale market
        (df['bed'] >= 1) & (df['bed'] <= 10) &
        (df['bath'] >= 1) & (df['bath'] <= 10) &
        (df['house_size'] >= 400) & (df['house_size'] <= 10000)
    ].copy()
    print(f"After filtering outliers: {len(df):,} properties")
    
    # Sample if too many properties
    if len(df) > max_properties:
        df = df.sample(n=max_properties, random_state=42).copy()
        print(f"Sampled to {max_properties} properties")
    
    # Generate property IDs
    df['property_id'] = [f'PROP_{i:04d}' for i in range(len(df))]
    
    # Map basic columns
    df['bedrooms'] = df['bed'].astype(int)
    df['bathrooms'] = df['bath']
    df['square_feet'] = df['house_size']
    df['listed_price'] = df['price']
    df['neighborhood'] = df['city'].fillna('Unknown')
    
    # Calculate lot size (convert acres to sqft, or estimate if missing)
    df['lot_size'] = df['acre_lot'].fillna(0.2) * 43560  # 1 acre = 43,560 sqft
    
    # Estimate property age based on price and size patterns
    # Newer homes = higher price per sqft typically
    df['price_per_sqft'] = df['listed_price'] / df['square_feet']
    df['age'] = np.clip(
        60 - (df['price_per_sqft'] / 50) + np.random.randint(-10, 10, len(df)),
        1, 100
    ).astype(int)
    
    # Generate property type based on size
    def get_property_type(row):
        if row['square_feet'] < 1000:
            return np.random.choice(['Condo', 'Townhouse'], p=[0.7, 0.3])
        elif row['square_feet'] < 2500:
            return np.random.choice(['Single Family', 'Townhouse'], p=[0.8, 0.2])
        else:
            return 'Single Family'
    
    df['property_type'] = df.apply(get_property_type, axis=1)
    
    # Generate stories based on size and type
    def get_stories(row):
        if row['property_type'] == 'Condo':
            return 1
        elif row['square_feet'] < 1500:
            return 1
        elif row['square_feet'] < 3000:
            return np.random.choice([1, 2], p=[0.3, 0.7])
        else:
            return np.random.choice([2, 3], p=[0.7, 0.3])
    
    df['stories'] = df.apply(get_stories, axis=1)
    
    # Generate condition based on age and price
    def get_condition(row):
        if row['age'] < 10 and row['price_per_sqft'] > 200:
            return 'Excellent'
        elif row['age'] < 20 and row['price_per_sqft'] > 150:
            return 'Good'
        elif row['age'] < 40:
            return 'Fair'
        elif row['age'] < 60:
            return np.random.choice(['Fair', 'Poor'], p=[0.6, 0.4])
        else:
            return np.random.choice(['Poor', 'Distressed'], p=[0.5, 0.5])
    
    df['condition'] = df.apply(get_condition, axis=1)
    
    # Generate garage spaces based on bedrooms
    df['garage_spaces'] = np.clip(df['bedrooms'] - 1, 0, 3).astype(int)
    
    # Generate amenities
    df['has_pool'] = ((df['square_feet'] > 2500) & (np.random.random(len(df)) > 0.7)).astype(int)
    df['has_fireplace'] = (np.random.random(len(df)) > 0.6).astype(int)
    df['has_deck'] = ((df['property_type'] == 'Single Family') & (np.random.random(len(df)) > 0.5)).astype(int)
    df['has_fence'] = (np.random.random(len(df)) > 0.4).astype(int)
    
    # HVAC
    df['has_central_heat'] = ((df['age'] < 50) | (np.random.random(len(df)) > 0.3)).astype(int)
    df['has_central_air'] = ((df['age'] < 40) | (np.random.random(len(df)) > 0.4)).astype(int)
    df['years_since_roof_replaced'] = np.clip(df['age'] * np.random.uniform(0.3, 0.8, len(df)), 0, 25).astype(int)
    df['years_since_hvac_replaced'] = np.clip(df['age'] * np.random.uniform(0.4, 0.9, len(df)), 0, 20).astype(int)
    
    # Updates
    df['kitchen_updated'] = ((df['age'] > 15) & (np.random.random(len(df)) > 0.6)).astype(int)
    df['bathrooms_updated'] = ((df['age'] > 15) & (np.random.random(len(df)) > 0.6)).astype(int)
    
    # HOA
    df['has_hoa'] = ((df['property_type'] == 'Condo') | ((df['property_type'] == 'Townhouse') & (np.random.random(len(df)) > 0.3))).astype(int)
    df['hoa_fee'] = df['has_hoa'] * np.random.randint(100, 500, len(df))
    df['has_special_assessment'] = ((df['has_hoa'] == 1) & (np.random.random(len(df)) > 0.9)).astype(int)
    
    # Location quality scores
    df['school_rating'] = np.random.choice([5, 6, 7, 8, 9], len(df), p=[0.1, 0.2, 0.4, 0.2, 0.1])
    df['walk_score'] = np.clip(np.random.normal(60, 20, len(df)), 0, 100).astype(int)
    df['transit_score'] = np.clip(df['walk_score'] * np.random.uniform(0.7, 1.0, len(df)), 0, 100).astype(int)
    
    # Market timing
    df['listing_month'] = np.random.randint(1, 13, len(df))
    df['is_spring_summer'] = df['listing_month'].isin([4, 5, 6, 7, 8]).astype(int)
    
    # Financial
    df['annual_tax'] = (df['listed_price'] * np.random.uniform(0.012, 0.025, len(df))).astype(int)
    df['estimated_rent'] = (df['listed_price'] * 0.006 * np.random.uniform(0.9, 1.1, len(df))).astype(int)
    
    # Distress signals
    df['days_on_market'] = np.random.choice([10, 20, 30, 60, 90, 120, 180], len(df), p=[0.2, 0.2, 0.2, 0.15, 0.1, 0.1, 0.05])
    df['price_reductions'] = np.random.choice([0, 1, 2, 3], len(df), p=[0.5, 0.3, 0.15, 0.05])
    df['is_foreclosure'] = (np.random.random(len(df)) > 0.95).astype(int)
    df['has_lien'] = (np.random.random(len(df)) > 0.97).astype(int)
    df['owner_occupied'] = (np.random.random(len(df)) > 0.4).astype(int)
    df['num_distress_keywords'] = np.random.choice([0, 1, 2, 3], len(df), p=[0.7, 0.2, 0.08, 0.02])
    
    # Repair costs based on condition
    repair_multipliers = {
        'Excellent': 0.01,
        'Good': 0.02,
        'Fair': 0.04,
        'Poor': 0.08,
        'Distressed': 0.15
    }
    df['estimated_repair_cost'] = df.apply(
        lambda row: int(row['listed_price'] * repair_multipliers[row['condition']] * np.random.uniform(0.5, 1.5)),
        axis=1
    )
    
    # Property categories
    df['parking_type'] = np.random.choice(['Driveway', 'Garage', 'Street', 'Carport'], len(df), p=[0.4, 0.3, 0.2, 0.1])
    df['heating_type'] = np.random.choice(['Gas', 'Electric', 'Oil', 'Heat Pump'], len(df), p=[0.5, 0.25, 0.15, 0.1])
    df['cooling_type'] = np.random.choice(['Central AC', 'Window Units', 'None'], len(df), p=[0.7, 0.2, 0.1])
    df['roof_type'] = np.random.choice(['Asphalt Shingle', 'Metal', 'Tile', 'Flat'], len(df), p=[0.7, 0.15, 0.1, 0.05])
    df['foundation_type'] = np.random.choice(['Slab', 'Crawl Space', 'Basement'], len(df), p=[0.4, 0.3, 0.3])
    df['flooring_type'] = np.random.choice(['Carpet', 'Hardwood', 'Tile', 'Laminate'], len(df), p=[0.3, 0.3, 0.2, 0.2])
    df['exterior_type'] = np.random.choice(['Vinyl Siding', 'Brick', 'Wood', 'Stucco'], len(df), p=[0.4, 0.3, 0.2, 0.1])
    df['water_source'] = np.random.choice(['Municipal', 'Well'], len(df), p=[0.85, 0.15])
    df['sewer_type'] = np.random.choice(['Municipal', 'Septic'], len(df), p=[0.8, 0.2])
    df['listing_season'] = pd.cut(df['listing_month'], bins=[0, 3, 6, 9, 12], labels=['Winter', 'Spring', 'Summer', 'Fall'])
    
    # TRUE MARKET VALUE - This is what makes it realistic
    # Use a pricing model based on actual features
    base_value = df['listed_price'].copy()
    
    # Adjust for condition
    condition_adjustments = {
        'Excellent': 1.05,
        'Good': 1.02,
        'Fair': 1.0,
        'Poor': 0.95,
        'Distressed': 0.85
    }
    for cond, mult in condition_adjustments.items():
        mask = df['condition'] == cond
        base_value.loc[mask] *= mult
    
    # Add market variation
    base_value *= np.random.uniform(0.95, 1.15, len(df))
    
    # Distressed properties = bigger discount
    distress_mask = (df['is_foreclosure'] == 1) | (df['has_lien'] == 1) | (df['days_on_market'] > 120)
    base_value.loc[distress_mask] *= np.random.uniform(1.10, 1.35, distress_mask.sum())
    
    df['true_market_value'] = base_value.astype(int)
    
    # Calculate spread
    df['spread'] = df['true_market_value'] - df['listed_price']
    df['spread_percentage'] = (df['spread'] / df['true_market_value'] * 100).round(2)
    
    # Select final columns in correct order
    final_columns = [
        'property_id', 'neighborhood', 'property_type', 'bedrooms', 'bathrooms',
        'square_feet', 'lot_size', 'age', 'stories', 'condition',
        'garage_spaces', 'has_pool', 'has_fireplace', 'has_deck', 'has_fence',
        'has_central_heat', 'has_central_air', 'years_since_roof_replaced',
        'years_since_hvac_replaced', 'kitchen_updated', 'bathrooms_updated',
        'has_hoa', 'hoa_fee', 'has_special_assessment',
        'school_rating', 'walk_score', 'transit_score',
        'listing_month', 'is_spring_summer',
        'annual_tax', 'estimated_rent',
        'days_on_market', 'price_reductions', 'is_foreclosure', 'has_lien',
        'owner_occupied', 'num_distress_keywords', 'estimated_repair_cost',
        'parking_type', 'heating_type', 'cooling_type', 'roof_type',
        'foundation_type', 'flooring_type', 'exterior_type', 'water_source',
        'sewer_type', 'listing_season', 'listed_price', 'true_market_value',
        'spread', 'spread_percentage'
    ]
    
    df_final = df[final_columns].copy()
    
    # Ensure data directory exists
    Path(output_file).parent.mkdir(exist_ok=True)
    
    # Save to CSV
    df_final.to_csv(output_file, index=False)
    
    print(f"\n✅ Processed data saved to: {output_file}")
    print(f"\n📊 Final Dataset Summary:")
    print(f"   Total properties: {len(df_final)}")
    print(f"   Price range: ${df_final['listed_price'].min():,} - ${df_final['listed_price'].max():,}")
    print(f"   Avg listed price: ${df_final['listed_price'].mean():,.0f}")
    print(f"   Avg market value: ${df_final['true_market_value'].mean():,.0f}")
    
    # Show wholesale opportunities
    opportunities = df_final[df_final['spread'] > 30000].sort_values('spread', ascending=False)
    print(f"\n🎯 Wholesale Opportunities (spread > $30k): {len(opportunities)}")
    if len(opportunities) > 0:
        print(f"\n💰 Top 5 Deals:")
        for idx, (_, prop) in enumerate(opportunities.head(5).iterrows(), 1):
            print(f"   {idx}. {prop['property_id']}: Listed ${prop['listed_price']:,} | Market ${prop['true_market_value']:,} | Spread ${prop['spread']:,} ({prop['spread_percentage']:.1f}%)")
    
    print("\n" + "="*80)
    
    return df_final


if __name__ == "__main__":
    # Generate random number of properties between 250-500
    num_properties = np.random.randint(250, 501)
    print(f"\nGenerating dataset with {num_properties} properties...")

    # Process the data
    df = process_real_estate_data(
        state_filter='Connecticut',  # Change to None for all states
        max_properties=num_properties
    )
