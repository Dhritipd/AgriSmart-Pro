"""
Training script for ML crop prediction model
COMPLETE VERSION FOR EXTENDED DATASET
"""
import sys
import os
from models.ml_predictor import MLCropPredictor

def main():
    """Train the ML model"""
    print("=" * 60)
    print("CROP PREDICTION MODEL TRAINING")
    print("Extended Dataset with Quality, Yield & Growth Duration")
    print("=" * 60)
    print()
    
    dataset_path = 'data/crop_recommendation.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: Dataset not found at '{dataset_path}'")
        print()
        print("Please ensure you have:")
        print("1. Created the 'data' folder in your project root")
        print("2. Placed 'crop_recommendation.csv' in the 'data' folder")
        print()
        print("Your CSV should have these columns:")
        print("N, P, K, temperature, humidity, ph, rainfall, label")
        print()
        print("Optional extended columns:")
        print("quality_score, yield_estimation, growth_duration")
        print()
        return
    
    print(f"✅ Dataset found: {dataset_path}")
    print()
    
    predictor = MLCropPredictor()
    
    print("🚀 Starting model training...")
    print("This may take a few moments...")
    print()
    
    try:
        results = predictor.train(dataset_path)
        
        print()
        print("=" * 60)
        print("✅ MODEL TRAINING COMPLETE!")
        print("=" * 60)
        print()
        
        print("🎯 CROP CLASSIFICATION RESULTS:")
        print(f"   • Accuracy: {results['crop_classification']['accuracy']}%")
        print(f"   • Cross-validation mean: {results['crop_classification']['cv_mean']}%")
        print(f"   • Cross-validation std: {results['crop_classification']['cv_std']}%")
        print(f"   • Training samples: {results['train_samples']}")
        print(f"   • Test samples: {results['test_samples']}")
        print()
        
        print("📈 Feature Importance (Crop Classification):")
        for feature, importance in sorted(
            results['crop_classification']['feature_importance'].items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            print(f"   • {feature:12s}: {importance:6.2f}%")
        print()
        
        if 'quality_score' in results:
            print("📊 QUALITY SCORE PREDICTION RESULTS:")
            print(f"   • RMSE: {results['quality_score']['rmse']}")
            print(f"   • R² Score: {results['quality_score']['r2_score']}")
            print(f"   • Accuracy: {results['quality_score']['accuracy_percentage']}%")
            print()
        
        if 'yield_estimation' in results:
            print("🌾 YIELD ESTIMATION RESULTS:")
            print(f"   • RMSE: {results['yield_estimation']['rmse']} t/ha")
            print(f"   • R² Score: {results['yield_estimation']['r2_score']}")
            print(f"   • Mean Yield: {results['yield_estimation']['mean_yield']} t/ha")
            print()
        
        if 'growth_duration' in results:
            print("⏱️ GROWTH DURATION PREDICTION RESULTS:")
            print(f"   • RMSE: {results['growth_duration']['rmse']} days")
            print(f"   • R² Score: {results['growth_duration']['r2_score']}")
            print(f"   • Mean Duration: {results['growth_duration']['mean_duration']} days")
            print()
        
        print("💾 Models saved successfully!")
        print(f"   Location: models/crop_model.pkl")
        print()
        print("=" * 60)
        print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("You can now run the Streamlit app:")
        print("   Command: streamlit run app.py")
        print()
        
    except Exception as e:
        print()
        print(f"❌ ERROR during training: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()