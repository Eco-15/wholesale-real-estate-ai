import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Remove fixed seed to generate different data each time
# Use time-based seed for truly random data
np.random.seed(int(datetime.now().timestamp()))

def generate_real_estate_data(n_properties=1000):
    """
    Generate realistic synthetic real estate data modeled after Stamford, Connecticut market
    """

    # Stamford, CT - Real neighborhoods and areas
    neighborhoods = [
        'Downtown/South End',    # Urban core, luxury condos
        'Shippan',              # Waterfront peninsula
        'Springdale',           # North Stamford, family homes
        'Glenbrook',            # East side, diverse housing
        'Turn of River',        # West side, suburban
        'North Stamford',       # Rural/estate properties
        'Cove',                 # Waterfront community
        'Belltown',             # Central residential
        'Newfield',             # Historic district
        'West Side',            # Mix of commercial/residential
        'High Ridge',           # North end, larger lots
        'Ridgeway'              # Residential neighborhood
    ]

    # Property types common in Stamford
    property_types = ['Single Family', 'Condo', 'Townhouse', 'Multi-Family']
    conditions = ['Excellent', 'Good', 'Fair', 'Poor', 'Distressed']

    # MLS-standard additional features (Northeast-specific)
    heating_types = ['Forced Air', 'Radiant', 'Heat Pump', 'Baseboard', 'Oil Heat']
    cooling_types = ['Central AC', 'Window Units', 'None', 'Heat Pump']
    parking_types = ['Garage', 'Carport', 'Driveway', 'Street', 'Covered']
    roof_types = ['Asphalt Shingle', 'Metal', 'Slate', 'Flat', 'Rubber']
    foundation_types = ['Slab', 'Crawl Space', 'Basement', 'Full Basement']
    flooring_types = ['Hardwood', 'Carpet', 'Tile', 'Laminate', 'Mixed']
    exterior_types = ['Vinyl', 'Brick', 'Wood', 'Stucco', 'Stone']

    # Stamford neighborhood price multipliers (based on actual market)
    # Stamford median home price is ~$550k-600k
    neighborhood_multipliers = {
        'Downtown/South End': 1.55,   # Luxury condos, high-rises ($800k-1.2M)
        'Shippan': 1.85,              # Waterfront premium ($1M-2M+)
        'Springdale': 1.10,           # North Stamford family homes ($600k-800k)
        'Glenbrook': 0.85,            # More affordable ($450k-600k)
        'Turn of River': 1.15,        # West side suburban ($650k-850k)
        'North Stamford': 1.65,       # Estate properties ($900k-1.5M)
        'Cove': 1.75,                 # Waterfront community ($950k-1.8M)
        'Belltown': 0.95,             # Central residential ($500k-700k)
        'Newfield': 1.05,             # Historic district ($550k-750k)
        'West Side': 0.90,            # Mixed use ($475k-650k)
        'High Ridge': 1.35,           # North end, larger lots ($700k-1M)
        'Ridgeway': 1.00,             # Standard residential ($525k-700k)
    }

    data = []

    for i in range(n_properties):
        # Stamford property distribution (based on actual market composition)
        neighborhood = np.random.choice(neighborhoods, p=[
            0.15,  # Downtown/South End (many condos)
            0.08,  # Shippan (exclusive waterfront)
            0.12,  # Springdale
            0.10,  # Glenbrook
            0.10,  # Turn of River
            0.08,  # North Stamford (estate area)
            0.06,  # Cove (small waterfront)
            0.08,  # Belltown
            0.07,  # Newfield
            0.08,  # West Side
            0.05,  # High Ridge
            0.03   # Ridgeway
        ])

        # Property type distribution (Stamford has MANY condos due to downtown)
        property_type = np.random.choice(property_types, p=[0.40, 0.35, 0.15, 0.10])
        
        # Size characteristics
        bedrooms = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.05, 0.15, 0.35, 0.30, 0.10, 0.05])
        bathrooms = max(1, bedrooms - np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1]))
        
        # Square footage (correlated with bedrooms)
        sqft_base = 600 + (bedrooms * 400)
        square_feet = int(np.random.normal(sqft_base, 300))
        square_feet = max(500, square_feet)
        
        # Age and condition
        year_built = np.random.randint(1950, 2024)
        age = 2024 - year_built
        
        # Condition based on age and randomness
        if age < 10:
            condition = np.random.choice(['Excellent', 'Good'], p=[0.7, 0.3])
        elif age < 30:
            condition = np.random.choice(['Good', 'Fair'], p=[0.6, 0.4])
        else:
            condition = np.random.choice(['Good', 'Fair', 'Poor'], p=[0.3, 0.5, 0.2])
        
        condition_multipliers = {
            'Excellent': 1.15,
            'Good': 1.0,
            'Fair': 0.85,
            'Poor': 0.70,
            'Distressed': 0.55
        }
        
        # Lot size
        lot_size = int(np.random.normal(8000, 3000))
        lot_size = max(2000, lot_size)

        # MLS-standard features
        garage_spaces = np.random.choice([0, 1, 2, 3], p=[0.15, 0.25, 0.45, 0.15])
        stories = np.random.choice([1, 2, 3], p=[0.60, 0.35, 0.05])
        has_pool = np.random.choice([0, 1], p=[0.85, 0.15])
        has_fireplace = np.random.choice([0, 1], p=[0.60, 0.40])
        has_deck = np.random.choice([0, 1], p=[0.55, 0.45])
        has_fence = np.random.choice([0, 1], p=[0.50, 0.50])

        # HVAC and systems
        heating_type = np.random.choice(heating_types)
        cooling_type = np.random.choice(cooling_types, p=[0.60, 0.15, 0.10, 0.15])
        has_central_heat = 1 if heating_type in ['Forced Air', 'Radiant', 'Heat Pump'] else 0
        has_central_air = 1 if cooling_type in ['Central AC', 'Heat Pump'] else 0

        # Structure features (Stamford/Northeast specific)
        parking_type = np.random.choice(parking_types, p=[0.55, 0.10, 0.20, 0.10, 0.05])  # More garages in CT
        roof_type = np.random.choice(roof_types, p=[0.65, 0.10, 0.15, 0.05, 0.05])  # More slate roofs in CT
        foundation_type = np.random.choice(foundation_types, p=[0.15, 0.20, 0.10, 0.55])  # Many full basements in CT
        flooring_type = np.random.choice(flooring_types, p=[0.35, 0.25, 0.15, 0.15, 0.10])  # More hardwood in CT
        exterior_type = np.random.choice(exterior_types, p=[0.30, 0.20, 0.20, 0.15, 0.15])  # Mix of siding types

        # Recent updates (affects value positively)
        years_since_roof_replaced = np.random.randint(0, min(age + 1, 30))
        years_since_hvac_replaced = np.random.randint(0, min(age + 1, 20))
        kitchen_updated = 1 if np.random.random() < 0.30 else 0
        bathrooms_updated = 1 if np.random.random() < 0.25 else 0

        # HOA and special assessments (Higher for Stamford condos)
        has_hoa = np.random.choice([0, 1], p=[0.50, 0.50])  # More HOAs in Stamford due to condos
        hoa_fee = int(np.random.uniform(200, 800)) if has_hoa else 0  # Higher HOA fees in CT
        has_special_assessment = 1 if (has_hoa and np.random.random() < 0.10) else 0

        # Utilities and services (Stamford is mostly public utilities)
        water_source = np.random.choice(['Public', 'Well'], p=[0.95, 0.05])  # Mostly public in city
        sewer_type = np.random.choice(['Public', 'Septic'], p=[0.92, 0.08])  # Mostly public sewer

        # School district (Stamford schools - mix of ratings)
        # Stamford has good schools overall, skew higher
        school_rating = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                        p=[0.02, 0.03, 0.05, 0.10, 0.15, 0.15, 0.20, 0.15, 0.10, 0.05])

        # Market timing features
        listing_month = np.random.randint(1, 13)
        listing_season = 'Spring' if listing_month in [3, 4, 5] else 'Summer' if listing_month in [6, 7, 8] else 'Fall' if listing_month in [9, 10, 11] else 'Winter'
        is_spring_summer = 1 if listing_season in ['Spring', 'Summer'] else 0

        # Walk/transit score (1-100) - Stamford has good walkability/transit
        # Higher scores for downtown, lower for north stamford
        if neighborhood in ['Downtown/South End', 'West Side', 'Belltown']:
            walk_score = np.random.randint(70, 100)  # Very walkable
            transit_score = np.random.randint(60, 95)  # Good transit
        elif neighborhood in ['Shippan', 'Cove', 'North Stamford']:
            walk_score = np.random.randint(20, 50)   # Less walkable
            transit_score = np.random.randint(10, 40)  # Limited transit
        else:
            walk_score = np.random.randint(40, 75)   # Moderate
            transit_score = np.random.randint(30, 65)  # Moderate transit

        # Calculate TRUE market value based on features
        # Stamford market: Higher base price to match ~$550k-600k median
        base_price = 200000  # Higher base for CT market
        price_per_sqft = 250 * neighborhood_multipliers[neighborhood]  # CT has higher $/sqft

        true_market_value = (
            base_price +
            (square_feet * price_per_sqft) +
            (bedrooms * 15000) +
            (bathrooms * 10000) +
            (lot_size * 5) -
            (age * 500) +
            (garage_spaces * 8000) +  # Garage adds value
            (school_rating * 5000) +  # Good schools add significant value
            (has_pool * 15000) +  # Pool adds value
            (has_fireplace * 5000) +
            (has_central_air * 8000) +
            (has_central_heat * 5000) +
            (kitchen_updated * 12000) +  # Updated kitchen is valuable
            (bathrooms_updated * 8000) -
            (years_since_roof_replaced * 300) -  # Old roof decreases value
            (years_since_hvac_replaced * 400) -  # Old HVAC decreases value
            (hoa_fee * 30) -  # High HOA fees decrease value
            (has_special_assessment * 10000)  # Special assessment is negative
        ) * condition_multipliers[condition]

        # Add some noise to make it realistic
        true_market_value *= np.random.normal(1.0, 0.05)
        true_market_value = int(true_market_value)

        # NOW calculate property tax and rental potential based on true_market_value
        annual_tax = int(true_market_value * np.random.uniform(0.008, 0.025))  # 0.8% to 2.5%
        estimated_rent = int(true_market_value * np.random.uniform(0.005, 0.012))  # Monthly rent estimate

        # Days on market (normal distribution, some outliers)
        days_on_market = max(1, int(np.random.exponential(30)))
        
        # Price reductions (correlated with days on market)
        if days_on_market > 60:
            price_reductions = np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1])
        elif days_on_market > 30:
            price_reductions = np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1])
        else:
            price_reductions = np.random.choice([0, 1], p=[0.8, 0.2])
        
        # Distress signals
        is_foreclosure = np.random.choice([0, 1], p=[0.95, 0.05])
        has_lien = np.random.choice([0, 1], p=[0.92, 0.08])
        owner_occupied = np.random.choice([0, 1], p=[0.3, 0.7])
        
        # Keywords in description (distress indicators)
        distress_keywords = ['motivated', 'as-is', 'handyman', 'tlc', 'estate sale', 'must sell']
        num_distress_keywords = 0
        if days_on_market > 45 or price_reductions > 1:
            num_distress_keywords = np.random.choice([0, 1, 2, 3], p=[0.4, 0.3, 0.2, 0.1])
        
        # Calculate LISTED price (what seller is asking)
        # Most properties listed at or slightly above market value
        # BUT we'll plant some undervalued opportunities
        
        listing_noise = np.random.normal(1.0, 0.08)  # Most within 8% of market value
        
        # Create different scenarios
        scenario = np.random.random()
        
        if scenario < 0.05:  # 5% - GREAT DEALS (what you want to find)
            # Significantly undervalued
            listed_price = true_market_value * np.random.uniform(0.70, 0.85)
            condition = np.random.choice(['Fair', 'Poor', 'Distressed'], p=[0.3, 0.4, 0.3])
            days_on_market = np.random.randint(45, 200)
            price_reductions = np.random.randint(1, 4)
            num_distress_keywords = np.random.randint(1, 4)
        elif scenario < 0.15:  # 10% - GOOD DEALS
            # Moderately undervalued
            listed_price = true_market_value * np.random.uniform(0.85, 0.93)
            days_on_market = max(days_on_market, 30)
        elif scenario < 0.70:  # 55% - FAIR MARKET VALUE
            # Listed at approximately market value
            listed_price = true_market_value * listing_noise
        else:  # 30% - OVERPRICED
            # Listed above market value
            listed_price = true_market_value * np.random.uniform(1.05, 1.25)
        
        listed_price = int(listed_price)
        
        # Estimated repair costs (higher for poor condition)
        if condition in ['Poor', 'Distressed']:
            repair_cost = int(np.random.uniform(15000, 50000))
        elif condition == 'Fair':
            repair_cost = int(np.random.uniform(5000, 20000))
        else:
            repair_cost = int(np.random.uniform(0, 10000))
        
        data.append({
            # Basic identifiers
            'property_id': f'PROP_{i+1:04d}',
            'neighborhood': neighborhood,
            'property_type': property_type,

            # Size and structure
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'square_feet': square_feet,
            'lot_size': lot_size,
            'stories': stories,
            'year_built': year_built,
            'age': age,
            'condition': condition,

            # Parking and garage
            'garage_spaces': garage_spaces,
            'parking_type': parking_type,

            # Amenities
            'has_pool': has_pool,
            'has_fireplace': has_fireplace,
            'has_deck': has_deck,
            'has_fence': has_fence,

            # HVAC and systems
            'heating_type': heating_type,
            'cooling_type': cooling_type,
            'has_central_heat': has_central_heat,
            'has_central_air': has_central_air,
            'years_since_roof_replaced': years_since_roof_replaced,
            'years_since_hvac_replaced': years_since_hvac_replaced,

            # Structure details
            'roof_type': roof_type,
            'foundation_type': foundation_type,
            'flooring_type': flooring_type,
            'exterior_type': exterior_type,

            # Updates and renovations
            'kitchen_updated': kitchen_updated,
            'bathrooms_updated': bathrooms_updated,

            # HOA and fees
            'has_hoa': has_hoa,
            'hoa_fee': hoa_fee,
            'has_special_assessment': has_special_assessment,

            # Utilities
            'water_source': water_source,
            'sewer_type': sewer_type,

            # Location quality
            'school_rating': school_rating,
            'walk_score': walk_score,
            'transit_score': transit_score,

            # Market timing
            'listing_month': listing_month,
            'listing_season': listing_season,
            'is_spring_summer': is_spring_summer,

            # Financial
            'annual_tax': annual_tax,
            'estimated_rent': estimated_rent,

            # Distress and market signals
            'days_on_market': days_on_market,
            'price_reductions': price_reductions,
            'is_foreclosure': is_foreclosure,
            'has_lien': has_lien,
            'owner_occupied': owner_occupied,
            'num_distress_keywords': num_distress_keywords,

            # Pricing
            'listed_price': listed_price,
            'true_market_value': true_market_value,
            'estimated_repair_cost': repair_cost
        })
    
    df = pd.DataFrame(data)
    
    # Calculate opportunity metrics (these would be calculated by your model in real life)
    df['spread'] = df['true_market_value'] - df['listed_price']
    df['spread_percentage'] = (df['spread'] / df['true_market_value'] * 100).round(2)
    
    return df

if __name__ == "__main__":
    # Ensure data directory exists
    Path('data').mkdir(exist_ok=True)

    # Stamford, CT market: ~300-500 active listings at any given time
    # Population ~135k, active real estate market
    # Generate realistic property count for Stamford market
    n_properties = np.random.randint(300, 501)
    print(f"Generating Stamford, Connecticut real estate market data...")
    print(f"Market snapshot: {n_properties} active listings...")
    df = generate_real_estate_data(n_properties=n_properties)

    # Save to CSV
    df.to_csv('data/real_estate_data.csv', index=False)
    
    print(f"\n✅ Generated {len(df)} properties")
    print(f"\n📊 Data Summary:")
    print(f"   Price range: ${df['listed_price'].min():,} - ${df['listed_price'].max():,}")
    print(f"   Avg listed price: ${df['listed_price'].mean():,.0f}")
    print(f"   Avg market value: ${df['true_market_value'].mean():,.0f}")
    
    # Show some good deals
    good_deals = df[df['spread'] > 30000].sort_values('spread', ascending=False).head(10)
    print(f"\n🎯 Planted {len(df[df['spread'] > 30000])} wholesale opportunities (spread > $30k)")
    print(f"\n💰 Top 5 Deals in Dataset:")
    for idx, row in good_deals.head(5).iterrows():
        print(f"   {row['property_id']}: Listed ${row['listed_price']:,} | "
              f"Market ${row['true_market_value']:,} | "
              f"Spread ${row['spread']:,} ({row['spread_percentage']:.1f}%)")
    
    print(f"\n✅ Data saved to: real_estate_data.csv")
