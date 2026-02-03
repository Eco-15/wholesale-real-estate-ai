#!/usr/bin/env python3
"""
FEEDBACK CLI TOOL
=================

Command-line interface for adding feedback and managing the learning system.

Usage:
    python3 feedback_cli.py add-feedback PROP_0123 500000 485000
    python3 feedback_cli.py summary
    python3 feedback_cli.py retrain
    python3 feedback_cli.py suggest
"""

import sys
import argparse
from feedback_learning import FeedbackLearningSystem
import pandas as pd

def add_feedback_interactive():
    """Interactive mode for adding feedback"""
    fls = FeedbackLearningSystem()

    print("\n" + "="*60)
    print("ADD FEEDBACK - INTERACTIVE MODE")
    print("="*60)

    property_id = input("\nProperty ID: ").strip()
    predicted_value = float(input("Predicted Market Value: $").replace(',', '').strip())
    actual_value = float(input("Actual Sale Price: $").replace(',', '').strip())

    print("\nFeedback Type:")
    print("  1. Actual Sale")
    print("  2. User Correction")
    print("  3. Deal Closed (Success)")
    print("  4. Deal Failed")
    feedback_type_choice = input("Choice (1-4): ").strip()

    feedback_types = {
        '1': 'actual_sale',
        '2': 'user_correction',
        '3': 'deal_closed',
        '4': 'deal_failed'
    }
    feedback_type = feedback_types.get(feedback_type_choice, 'actual_sale')

    deal_outcome = None
    if feedback_type_choice in ['3', '4']:
        deal_outcome = 'success' if feedback_type_choice == '3' else 'failed'

    user_confidence = input("Confidence (1-10, optional): ").strip()
    user_confidence = int(user_confidence) if user_confidence else None

    notes = input("Notes (optional): ").strip()

    should_retrain = fls.add_feedback(
        property_id=property_id,
        predicted_value=predicted_value,
        actual_value=actual_value,
        feedback_type=feedback_type,
        deal_outcome=deal_outcome,
        user_confidence=user_confidence,
        notes=notes
    )

    if should_retrain:
        retrain = input("\n🤔 Retrain model now? (y/n): ").strip().lower()
        if retrain == 'y':
            fls.incremental_retrain()

def add_feedback_cli(args):
    """Add feedback via command line"""
    fls = FeedbackLearningSystem()

    should_retrain = fls.add_feedback(
        property_id=args.property_id,
        predicted_value=args.predicted_value,
        actual_value=args.actual_value,
        feedback_type=args.feedback_type,
        deal_outcome=args.deal_outcome,
        user_confidence=args.confidence,
        notes=args.notes
    )

    if should_retrain and args.auto_retrain:
        print("\n🔄 Auto-retraining enabled...")
        fls.incremental_retrain()

def show_summary(args):
    """Show feedback summary"""
    fls = FeedbackLearningSystem()

    print("\n" + "="*60)
    print("FEEDBACK SUMMARY")
    print("="*60)

    summary = fls.get_feedback_summary()

    if isinstance(summary, dict):
        print(f"\n📊 Statistics:")
        print(f"   Total feedback entries: {summary['total_feedback']}")
        print(f"   Average error: ${summary['avg_error']:,.0f} ({summary['avg_error_pct']:.2f}%)")
        print(f"   Mean Absolute Error: ${summary['mae']:,.0f}")

        print(f"\n📈 Feedback by Type:")
        for ftype, count in summary['feedback_by_type'].items():
            print(f"   {ftype}: {count}")

        print(f"\n💼 Deal Outcomes:")
        print(f"   Successful deals: {summary['deals_closed']}")
        print(f"   Failed deals: {summary['deals_failed']}")

        if summary['deals_closed'] + summary['deals_failed'] > 0:
            success_rate = summary['deals_closed'] / (summary['deals_closed'] + summary['deals_failed']) * 100
            print(f"   Success rate: {success_rate:.1f}%")
    else:
        print(f"\n{summary}")

    # Show learning log
    import json
    from pathlib import Path
    log_path = 'data/learning_log.json'
    if Path(log_path).exists():
        with open(log_path, 'r') as f:
            log = json.load(f)

        print(f"\n🤖 Model Info:")
        print(f"   Current version: {log['model_version']}")
        print(f"   Last retrain: {log['last_retrain'] or 'Never'}")
        print(f"   Total feedback used: {log['feedback_count']}")

        if log['performance_history']:
            print(f"\n📈 Performance History:")
            for perf in log['performance_history'][-5:]:  # Last 5
                print(f"   v{perf['version']}: MAE ${perf['mae']:,.0f}, R² {perf['r2']:.4f}")

def retrain_model(args):
    """Retrain the model with feedback"""
    fls = FeedbackLearningSystem()
    result = fls.incremental_retrain()

    if result:
        print(f"\n✅ Model retrained successfully!")
        print(f"   New version: {result['version']}")
        print(f"   Performance on feedback data:")
        print(f"   - MAE: ${result['mae']:,.0f}")
        print(f"   - R²: {result['r2']:.4f}")

def suggest_feedback(args):
    """Suggest properties that would benefit from feedback"""
    fls = FeedbackLearningSystem()

    # Load opportunities
    opportunities_path = 'data/real_estate_data_opportunities.csv'
    from pathlib import Path
    if not Path(opportunities_path).exists():
        print("❌ No opportunities data found. Run use_model.py first.")
        return

    opportunities = pd.read_csv(opportunities_path)
    fls.suggest_properties_for_feedback(opportunities, n=args.n)

def main():
    parser = argparse.ArgumentParser(
        description='Feedback Learning System CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add feedback interactively
  python3 feedback_cli.py add

  # Add feedback via command line
  python3 feedback_cli.py add-feedback PROP_0123 500000 485000

  # Show feedback summary
  python3 feedback_cli.py summary

  # Retrain model
  python3 feedback_cli.py retrain

  # Get suggestions for which properties need feedback
  python3 feedback_cli.py suggest
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Add feedback command (interactive)
    subparsers.add_parser('add', help='Add feedback interactively')

    # Add feedback command (CLI)
    add_parser = subparsers.add_parser('add-feedback', help='Add feedback via CLI')
    add_parser.add_argument('property_id', help='Property ID')
    add_parser.add_argument('predicted_value', type=float, help='Predicted value')
    add_parser.add_argument('actual_value', type=float, help='Actual sale price')
    add_parser.add_argument('--type', dest='feedback_type', default='actual_sale',
                           choices=['actual_sale', 'user_correction', 'deal_closed', 'deal_failed'],
                           help='Type of feedback')
    add_parser.add_argument('--outcome', dest='deal_outcome',
                           choices=['success', 'failed'],
                           help='Deal outcome')
    add_parser.add_argument('--confidence', type=int, choices=range(1, 11),
                           help='Confidence score (1-10)')
    add_parser.add_argument('--notes', default='', help='Additional notes')
    add_parser.add_argument('--auto-retrain', action='store_true',
                           help='Automatically retrain if threshold reached')

    # Summary command
    subparsers.add_parser('summary', help='Show feedback summary')

    # Retrain command
    subparsers.add_parser('retrain', help='Retrain model with feedback')

    # Suggest command
    suggest_parser = subparsers.add_parser('suggest', help='Suggest properties for feedback')
    suggest_parser.add_argument('-n', type=int, default=10,
                               help='Number of suggestions (default: 10)')

    args = parser.parse_args()

    if args.command == 'add':
        add_feedback_interactive()
    elif args.command == 'add-feedback':
        add_feedback_cli(args)
    elif args.command == 'summary':
        show_summary(args)
    elif args.command == 'retrain':
        retrain_model(args)
    elif args.command == 'suggest':
        suggest_feedback(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
