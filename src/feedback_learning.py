"""
FEEDBACK-BASED INCREMENTAL LEARNING SYSTEM
==========================================

This module implements a feedback loop where the model learns from:
1. Actual sale prices (ground truth)
2. User corrections on valuations
3. Deal outcomes (success/failure)

The model progressively improves as more feedback is collected.
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
from datetime import datetime
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, r2_score

class FeedbackLearningSystem:
    """
    Implements incremental learning from user feedback
    """

    def __init__(self, model_path='models/wholesale_model.pkl'):
        self.model_path = model_path
        self.feedback_db_path = 'data/feedback_database.csv'
        self.learning_log_path = 'data/learning_log.json'
        self.model = None
        self.load_model()
        self.initialize_feedback_db()

    def load_model(self):
        """Load the trained model"""
        if Path(self.model_path).exists():
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.label_encoders = model_data['label_encoders']
                self.feature_columns = model_data['feature_columns']
                print(f"✅ Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError("Model not found. Train the model first.")

    def initialize_feedback_db(self):
        """Initialize feedback database if it doesn't exist"""
        if not Path(self.feedback_db_path).exists():
            # Create empty feedback database
            df = pd.DataFrame(columns=[
                'feedback_id', 'property_id', 'timestamp', 'feedback_type',
                'predicted_value', 'actual_value', 'error', 'deal_outcome',
                'user_confidence', 'notes'
            ])
            df.to_csv(self.feedback_db_path, index=False)
            print(f"✅ Created feedback database at {self.feedback_db_path}")

        if not Path(self.learning_log_path).exists():
            # Create learning log
            log = {
                'model_version': 1,
                'last_retrain': None,
                'feedback_count': 0,
                'performance_history': []
            }
            with open(self.learning_log_path, 'w') as f:
                json.dump(log, f, indent=2)
            print(f"✅ Created learning log at {self.learning_log_path}")

    def add_feedback(self, property_id, predicted_value, actual_value,
                     feedback_type='actual_sale', deal_outcome=None,
                     user_confidence=None, notes=''):
        """
        Add feedback to the database

        Parameters:
        -----------
        property_id : str
            Property identifier
        predicted_value : float
            Model's predicted market value
        actual_value : float
            Actual sale price or corrected value
        feedback_type : str
            'actual_sale', 'user_correction', 'deal_closed', 'deal_failed'
        deal_outcome : str
            'success', 'failed', None
        user_confidence : float
            Confidence score 1-10
        notes : str
            Additional notes
        """
        # Load feedback database
        feedback_df = pd.read_csv(self.feedback_db_path)

        # Calculate error
        error = actual_value - predicted_value
        error_pct = (error / actual_value) * 100

        # Create feedback entry
        feedback_entry = {
            'feedback_id': f"FB_{len(feedback_df) + 1:05d}",
            'property_id': property_id,
            'timestamp': datetime.now().isoformat(),
            'feedback_type': feedback_type,
            'predicted_value': predicted_value,
            'actual_value': actual_value,
            'error': error,
            'error_pct': error_pct,
            'deal_outcome': deal_outcome,
            'user_confidence': user_confidence,
            'notes': notes
        }

        # Append to database
        feedback_df = pd.concat([feedback_df, pd.DataFrame([feedback_entry])], ignore_index=True)
        feedback_df.to_csv(self.feedback_db_path, index=False)

        # Update learning log
        with open(self.learning_log_path, 'r') as f:
            log = json.load(f)
        log['feedback_count'] = len(feedback_df)
        with open(self.learning_log_path, 'w') as f:
            json.dump(log, f, indent=2)

        print(f"✅ Feedback added: {feedback_entry['feedback_id']}")
        print(f"   Property: {property_id}")
        print(f"   Predicted: ${predicted_value:,.0f}")
        print(f"   Actual: ${actual_value:,.0f}")
        print(f"   Error: ${error:,.0f} ({error_pct:.2f}%)")

        # Check if we should retrain
        if len(feedback_df) % 10 == 0:  # Retrain every 10 feedbacks
            print(f"\n📊 {len(feedback_df)} feedback entries collected. Consider retraining!")
            return True

        return False

    def get_feedback_summary(self):
        """Get summary statistics of feedback"""
        if not Path(self.feedback_db_path).exists():
            return None

        feedback_df = pd.read_csv(self.feedback_db_path)

        if len(feedback_df) == 0:
            return "No feedback collected yet."

        summary = {
            'total_feedback': len(feedback_df),
            'avg_error': feedback_df['error'].mean(),
            'avg_error_pct': feedback_df['error_pct'].mean(),
            'mae': feedback_df['error'].abs().mean(),
            'feedback_by_type': feedback_df['feedback_type'].value_counts().to_dict(),
            'deals_closed': len(feedback_df[feedback_df['deal_outcome'] == 'success']),
            'deals_failed': len(feedback_df[feedback_df['deal_outcome'] == 'failed']),
        }

        return summary

    def incremental_retrain(self, original_data_path='data/real_estate_data.csv'):
        """
        Retrain the model incrementally with feedback data

        This combines:
        1. Original training data
        2. Feedback data with actual values
        3. Uses higher weights for feedback data (more recent = more important)
        """
        print("\n" + "="*80)
        print("🔄 INCREMENTAL RETRAINING WITH FEEDBACK")
        print("="*80)

        # Load original data
        original_df = pd.read_csv(original_data_path)
        print(f"📊 Loaded {len(original_df)} properties from original dataset")

        # Load feedback data
        feedback_df = pd.read_csv(self.feedback_db_path)

        if len(feedback_df) == 0:
            print("❌ No feedback data available for retraining")
            return

        print(f"📊 Loaded {len(feedback_df)} feedback entries")

        # Merge feedback with original properties to get features
        feedback_properties = []
        for _, feedback in feedback_df.iterrows():
            # Find the property in original data
            prop = original_df[original_df['property_id'] == feedback['property_id']]
            if len(prop) > 0:
                prop = prop.copy()
                # Update the true market value with actual feedback value
                prop['true_market_value'] = feedback['actual_value']
                prop['feedback_weight'] = 2.0  # Give feedback data higher weight
                feedback_properties.append(prop)

        if len(feedback_properties) == 0:
            print("❌ No matching properties found for feedback")
            return

        feedback_df_merged = pd.concat(feedback_properties, ignore_index=True)
        print(f"✅ Merged {len(feedback_df_merged)} feedback properties with features")

        # Add weight column to original data
        original_df['feedback_weight'] = 1.0

        # Combine datasets
        combined_df = pd.concat([original_df, feedback_df_merged], ignore_index=True)
        print(f"📊 Combined dataset: {len(combined_df)} properties")

        # Prepare features (reuse the model's prepare_features method)
        from wholesale_model import RealEstateWholesaleModel
        temp_model = RealEstateWholesaleModel()
        temp_model.label_encoders = self.label_encoders
        temp_model.feature_columns = self.feature_columns

        combined_df_processed, X = temp_model.prepare_features(combined_df, fit_encoders=False)
        y = combined_df_processed['true_market_value']
        weights = combined_df_processed['feedback_weight']

        # Retrain model with sample weights
        print("\n🚀 Retraining model with feedback...")
        self.model.fit(X, y, sample_weight=weights, verbose=False)

        # Evaluate on feedback data only
        feedback_X = X[-len(feedback_df_merged):]
        feedback_y = y[-len(feedback_df_merged):]
        predictions = self.model.predict(feedback_X)

        mae = mean_absolute_error(feedback_y, predictions)
        r2 = r2_score(feedback_y, predictions)

        print(f"\n📈 Performance on Feedback Data:")
        print(f"   MAE: ${mae:,.0f}")
        print(f"   R²: {r2:.4f}")

        # Save updated model
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'results': {'mae': mae, 'r2': r2}
        }

        # Backup old model
        backup_path = f"{self.model_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if Path(self.model_path).exists():
            import shutil
            shutil.copy(self.model_path, backup_path)
            print(f"💾 Old model backed up to {backup_path}")

        # Save new model
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"💾 Updated model saved to {self.model_path}")

        # Update learning log
        with open(self.learning_log_path, 'r') as f:
            log = json.load(f)

        log['model_version'] += 1
        log['last_retrain'] = datetime.now().isoformat()
        log['performance_history'].append({
            'version': log['model_version'],
            'timestamp': datetime.now().isoformat(),
            'feedback_count': len(feedback_df),
            'mae': float(mae),
            'r2': float(r2)
        })

        with open(self.learning_log_path, 'w') as f:
            json.dump(log, f, indent=2)

        print("\n✅ Incremental retraining complete!")
        print(f"📊 Model version: {log['model_version']}")

        return {
            'version': log['model_version'],
            'mae': mae,
            'r2': r2,
            'feedback_count': len(feedback_df)
        }

    def suggest_properties_for_feedback(self, predictions_df, n=10):
        """
        Use active learning to identify properties where feedback would be most valuable

        Properties with:
        - High uncertainty (large predicted spread but low confidence)
        - Near decision boundaries
        - Unusual feature combinations
        """
        # Calculate uncertainty score
        predictions_df['uncertainty_score'] = (
            predictions_df['predicted_spread_pct'] / 100 +  # High spread = uncertain
            (1 / (predictions_df['days_on_market'] + 1))    # New listings = uncertain
        )

        # Sort by uncertainty
        uncertain_properties = predictions_df.nlargest(n, 'uncertainty_score')

        print(f"\n🎯 Top {n} Properties Recommended for Feedback:")
        print("   (Model is most uncertain about these - feedback would help most)")
        print()

        for idx, (_, prop) in enumerate(uncertain_properties.iterrows(), 1):
            print(f"{idx}. {prop['property_id']} - {prop['neighborhood']}")
            print(f"   Predicted Value: ${prop['predicted_market_value']:,.0f}")
            print(f"   Uncertainty Score: {prop['uncertainty_score']:.2f}")
            print()

        return uncertain_properties


def demo_feedback_system():
    """Demonstrate the feedback learning system"""
    print("="*80)
    print("FEEDBACK-BASED LEARNING SYSTEM DEMO")
    print("="*80)

    # Initialize system
    fls = FeedbackLearningSystem()

    # Show current feedback summary
    print("\n📊 Current Feedback Summary:")
    summary = fls.get_feedback_summary()
    if isinstance(summary, dict):
        print(f"   Total feedback entries: {summary['total_feedback']}")
        print(f"   Average error: ${summary['avg_error']:,.0f}")
        print(f"   Mean Absolute Error: ${summary['mae']:,.0f}")
        print(f"   Deals closed: {summary['deals_closed']}")
        print(f"   Deals failed: {summary['deals_failed']}")
    else:
        print(f"   {summary}")

    print("\n" + "="*80)
    print("HOW TO USE:")
    print("="*80)
    print()
    print("1. ADD FEEDBACK when a property closes:")
    print("   fls.add_feedback(")
    print("       property_id='PROP_0123',")
    print("       predicted_value=500000,")
    print("       actual_value=485000,")
    print("       feedback_type='actual_sale',")
    print("       deal_outcome='success'")
    print("   )")
    print()
    print("2. RETRAIN MODEL after collecting feedback:")
    print("   fls.incremental_retrain()")
    print()
    print("3. GET SUGGESTIONS for which properties need feedback:")
    print("   fls.suggest_properties_for_feedback(opportunities_df)")
    print()


if __name__ == "__main__":
    demo_feedback_system()
