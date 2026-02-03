import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pickle
import json
from pathlib import Path

class RealEstateWholesaleModel:
    """
    XGBoost model for predicting real estate market values and finding wholesale opportunities
    """
    
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = None
        self.results = {}
        
    def prepare_features(self, df, fit_encoders=False):
        """
        Prepare features for model training/prediction
        """
        df = df.copy()
        
        # Categorical columns that need encoding
        categorical_cols = [
            'neighborhood', 'property_type', 'condition',
            'parking_type', 'heating_type', 'cooling_type',
            'roof_type', 'foundation_type', 'flooring_type', 'exterior_type',
            'water_source', 'sewer_type', 'listing_season'
        ]

        for col in categorical_cols:
            if col in df.columns:
                if fit_encoders:
                    # Create and fit encoder
                    le = LabelEncoder()
                    df[col + '_encoded'] = le.fit_transform(df[col])
                    self.label_encoders[col] = le
                else:
                    # Use existing encoder
                    df[col + '_encoded'] = self.label_encoders[col].transform(df[col])
        
        # Feature engineering - create new features
        df['price_per_sqft'] = df['listed_price'] / df['square_feet']
        df['age_condition_interaction'] = df['age'] * df['condition_encoded']
        df['is_distressed'] = ((df['days_on_market'] > 60) | 
                               (df['price_reductions'] > 1) | 
                               (df['num_distress_keywords'] > 0)).astype(int)
        df['distress_score'] = (df['days_on_market'] / 10 + 
                               df['price_reductions'] * 10 + 
                               df['num_distress_keywords'] * 5 +
                               df['is_foreclosure'] * 20 +
                               df['has_lien'] * 15)
        
        # Select features for model - MLS-standard comprehensive feature set
        feature_cols = [
            # Core property features
            'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'age', 'stories',

            # Parking and garage
            'garage_spaces',

            # Amenities
            'has_pool', 'has_fireplace', 'has_deck', 'has_fence',

            # HVAC and systems
            'has_central_heat', 'has_central_air',
            'years_since_roof_replaced', 'years_since_hvac_replaced',

            # Updates and renovations
            'kitchen_updated', 'bathrooms_updated',

            # HOA and fees
            'has_hoa', 'hoa_fee', 'has_special_assessment',

            # Location quality
            'school_rating', 'walk_score', 'transit_score',

            # Market timing
            'listing_month', 'is_spring_summer',

            # Financial
            'annual_tax', 'estimated_rent',

            # Distress signals
            'days_on_market', 'price_reductions', 'is_foreclosure', 'has_lien',
            'owner_occupied', 'num_distress_keywords',

            # Repair and condition
            'estimated_repair_cost',

            # Encoded categorical features
            'neighborhood_encoded', 'property_type_encoded', 'condition_encoded',
            'parking_type_encoded', 'heating_type_encoded', 'cooling_type_encoded',
            'roof_type_encoded', 'foundation_type_encoded', 'flooring_type_encoded',
            'exterior_type_encoded', 'water_source_encoded', 'sewer_type_encoded',
            'listing_season_encoded',

            # Engineered features
            'price_per_sqft', 'age_condition_interaction', 'distress_score'
        ]

        # Filter to only include features that exist in the dataframe
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        self.feature_columns = feature_cols
        
        return df, df[feature_cols]
    
    def train(self, df, target_col='true_market_value'):
        """
        Train XGBoost model on the data
        """
        print("🔨 Preparing features...")
        df_processed, X = self.prepare_features(df, fit_encoders=True)
        y = df_processed[target_col]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"📊 Training set: {len(X_train)} properties")
        print(f"📊 Test set: {len(X_test)} properties")
        
        # Train XGBoost model with DEEP FOREST (1000 trees)
        print("\n🚀 Training XGBoost model with deep forest (1000 trees)...")
        print(f"📊 Using {len(self.feature_columns)} features for training")

        self.model = xgb.XGBRegressor(
            n_estimators=1000,          # 5x more trees for deeper analysis
            learning_rate=0.03,          # Slower learning for more precision
            max_depth=8,                 # Deeper trees to capture complex patterns
            min_child_weight=2,          # Allow more splits for nuanced patterns
            subsample=0.85,              # Use more data per tree
            colsample_bytree=0.85,       # Use more features per tree
            gamma=0.1,                   # Min loss reduction for split (prevents overfitting)
            reg_alpha=0.05,              # L1 regularization
            reg_lambda=1.0,              # L2 regularization
            random_state=42,
            n_jobs=-1,                   # Use all CPU cores
            tree_method='hist',          # Faster histogram-based method
            early_stopping_rounds=50     # Stop if no improvement for 50 rounds
        )
        
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        # Make predictions
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        # Calculate metrics
        train_mae = mean_absolute_error(y_train, train_pred)
        test_mae = mean_absolute_error(y_test, test_pred)
        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        
        # Calculate MAPE
        train_mape = np.mean(np.abs((y_train - train_pred) / y_train)) * 100
        test_mape = np.mean(np.abs((y_test - test_pred) / y_test)) * 100
        
        self.results = {
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_mape': train_mape,
            'test_mape': test_mape
        }
        
        print("\n✅ Model Training Complete!")
        print(f"\n📈 Model Performance:")
        print(f"   Train MAE: ${train_mae:,.0f} (avg $ off)")
        print(f"   Test MAE:  ${test_mae:,.0f} (avg $ off)")
        print(f"   Train MAPE: {train_mape:.2f}% (avg % error)")
        print(f"   Test MAPE:  {test_mape:.2f}% (avg % error)")
        print(f"   Train R²: {train_r2:.4f}")
        print(f"   Test R²:  {test_r2:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\n🎯 Top 10 Most Important Features:")
        for idx, row in feature_importance.head(10).iterrows():
            print(f"   {row['feature']:<30} {row['importance']:.4f}")
        
        return self.results
    
    def predict(self, df):
        """
        Predict market values for properties
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        df_processed, X = self.prepare_features(df, fit_encoders=False)
        predictions = self.model.predict(X)
        
        return predictions
    
    def find_opportunities(self, df, min_spread=20000, min_spread_pct=10):
        """
        Find wholesale opportunities in the dataset
        """
        print("\n🔍 Analyzing properties for wholesale opportunities...")
        
        # Make predictions
        predicted_values = self.predict(df)
        
        # Create results dataframe
        results = df.copy()
        results['predicted_market_value'] = predicted_values.astype(int)
        results['predicted_spread'] = results['predicted_market_value'] - results['listed_price']
        results['predicted_spread_pct'] = (results['predicted_spread'] / results['predicted_market_value'] * 100).round(2)
        
        # Calculate prediction error (only available with synthetic data)
        if 'true_market_value' in results.columns:
            results['prediction_error'] = results['predicted_market_value'] - results['true_market_value']
            results['prediction_error_pct'] = (results['prediction_error'] / results['true_market_value'] * 100).round(2)
        
        # Distress score (higher = more distressed = better opportunity)
        results['distress_score'] = (
            results['days_on_market'] / 10 + 
            results['price_reductions'] * 10 + 
            results['num_distress_keywords'] * 5 +
            results['is_foreclosure'] * 20 +
            results['has_lien'] * 15
        )
        
        # Calculate estimated profit (conservative)
        wholesale_fee = 10000  # Your fee
        closing_costs = 5000   # Closing costs
        results['estimated_profit'] = results['predicted_spread'] - results['estimated_repair_cost'] - wholesale_fee - closing_costs
        
        # Opportunity score (weighted combination of factors)
        results['opportunity_score'] = (
            (results['predicted_spread_pct'] * 2) +  # Spread percentage (most important)
            (results['distress_score'] / 5) +         # Distress signals
            (results['estimated_profit'] / 10000)     # Profit potential
        ).round(2)
        
        # Filter for good opportunities
        opportunities = results[
            (results['predicted_spread'] >= min_spread) &
            (results['predicted_spread_pct'] >= min_spread_pct) &
            (results['estimated_profit'] > 0)
        ].sort_values('opportunity_score', ascending=False)
        
        print(f"\n✅ Found {len(opportunities)} wholesale opportunities")
        print(f"   (min spread: ${min_spread:,}, min spread %: {min_spread_pct}%)")
        
        return opportunities, results
    
    def save_model(self, filepath='models/wholesale_model.pkl'):
        """
        Save trained model to disk
        """
        # Ensure models directory exists
        Path(filepath).parent.mkdir(exist_ok=True)

        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'results': self.results
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"\n💾 Model saved to: {filepath}")
    
    def load_model(self, filepath='models/wholesale_model.pkl'):
        """
        Load trained model from disk
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        self.results = model_data['results']
        
        print(f"\n📂 Model loaded from: {filepath}")


def main():
    """
    Main execution function
    """
    print("=" * 80)
    print("🏠 REAL ESTATE WHOLESALE OPPORTUNITY FINDER")
    print("=" * 80)
    
    # Load data
    print("\n📁 Loading data...")
    df = pd.read_csv('data/real_estate_data.csv')
    print(f"✅ Loaded {len(df)} properties")
    
    # Initialize and train model
    model = RealEstateWholesaleModel()
    model.train(df)
    
    # Find opportunities
    opportunities, all_results = model.find_opportunities(
        df, 
        min_spread=20000,      # Minimum $20k spread
        min_spread_pct=10      # Minimum 10% spread
    )
    
    # Display top opportunities
    print("\n" + "=" * 80)
    print("💰 TOP 20 WHOLESALE OPPORTUNITIES")
    print("=" * 80)
    
    display_cols = [
        'property_id', 'neighborhood', 'property_type', 'bedrooms', 'bathrooms',
        'square_feet', 'condition', 'days_on_market', 'price_reductions',
        'listed_price', 'predicted_market_value', 'predicted_spread', 
        'predicted_spread_pct', 'estimated_repair_cost', 'estimated_profit',
        'distress_score', 'opportunity_score'
    ]
    
    for idx, (_, row) in enumerate(opportunities.head(20).iterrows(), 1):
        print(f"\n🎯 #{idx} - {row['property_id']} (Score: {row['opportunity_score']:.1f})")
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
        
        # Show actual value if available (synthetic data only)
        if 'true_market_value' in row:
            print(f"   🎯 Actual Market Value: ${row['true_market_value']:,} "
                  f"(Error: ${abs(row['prediction_error']):,})")
    
    # Save results
    opportunities.to_csv('wholesale_opportunities.csv', index=False)
    all_results.to_csv('all_properties_analyzed.csv', index=False)
    
    print("\n" + "=" * 80)
    print("📊 SUMMARY STATISTICS")
    print("=" * 80)
    print(f"✅ Total opportunities found: {len(opportunities)}")
    print(f"💰 Avg predicted spread: ${opportunities['predicted_spread'].mean():,.0f}")
    print(f"💰 Avg estimated profit: ${opportunities['estimated_profit'].mean():,.0f}")
    print(f"📈 Avg opportunity score: {opportunities['opportunity_score'].mean():.2f}")
    
    # Model accuracy on identified opportunities
    if 'true_market_value' in opportunities.columns:
        avg_error = opportunities['prediction_error'].abs().mean()
        avg_error_pct = opportunities['prediction_error_pct'].abs().mean()
        print(f"\n🎯 Model Accuracy on Opportunities:")
        print(f"   Average prediction error: ${avg_error:,.0f} ({avg_error_pct:.2f}%)")
    
    print("\n📁 Files saved:")
    print(f"   • wholesale_opportunities.csv - Top opportunities ranked")
    print(f"   • all_properties_analyzed.csv - All properties with predictions")
    
    # Save model
    model.save_model()
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    
    return model, opportunities, all_results


if __name__ == "__main__":
    model, opportunities, all_results = main()
