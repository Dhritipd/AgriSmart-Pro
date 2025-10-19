"""
Machine Learning based Crop Recommendation System
COMPLETE VERSION FOR EXTENDED DATASET
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class MLCropPredictor:
    """ML-based crop predictor with extended metrics support"""
    
    def __init__(self, model_path='models/crop_model.pkl'):
        self.model_path = model_path
        self.classifier_model = None
        self.quality_model = None
        self.yield_model = None
        self.duration_model = None
        self.scaler = None
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        
        if os.path.exists(model_path):
            self.load_model()
    
    def train(self, data_path='data/crop_recommendation.csv', test_size=0.2):
        """Train all ML models"""
        df = pd.read_csv(data_path)
        
        print(f"📊 Dataset loaded: {len(df)} samples")
        print(f"📋 Columns: {list(df.columns)}")
        print(f"🌾 Unique crops: {df['label'].nunique()}")
        
        X = df[self.feature_names]
        y_crop = df['label']
        
        has_quality = 'quality_score' in df.columns
        has_yield = 'yield_estimation' in df.columns
        has_duration = 'growth_duration' in df.columns
        
        print(f"\n📈 Extended features:")
        print(f"   • Quality Score: {'✅' if has_quality else '❌'}")
        print(f"   • Yield Estimation: {'✅' if has_yield else '❌'}")
        print(f"   • Growth Duration: {'✅' if has_duration else '❌'}")
        
        X_train, X_test, y_crop_train, y_crop_test = train_test_split(
            X, y_crop, test_size=test_size, random_state=42, stratify=y_crop
        )
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        results = {}
        
        # Crop Classification
        print("\n🎯 Training Crop Classification...")
        self.classifier_model = RandomForestClassifier(
            n_estimators=200, max_depth=20, min_samples_split=5,
            min_samples_leaf=2, random_state=42, n_jobs=-1
        )
        self.classifier_model.fit(X_train_scaled, y_crop_train)
        y_pred = self.classifier_model.predict(X_test_scaled)
        
        accuracy = accuracy_score(y_crop_test, y_pred)
        cv_scores = cross_val_score(self.classifier_model, X_train_scaled, y_crop_train, cv=5)
        
        results['crop_classification'] = {
            'accuracy': round(accuracy * 100, 2),
            'cv_mean': round(cv_scores.mean() * 100, 2),
            'cv_std': round(cv_scores.std() * 100, 2),
            'feature_importance': dict(zip(
                self.feature_names,
                [round(imp * 100, 2) for imp in self.classifier_model.feature_importances_]
            ))
        }
        print(f"   ✅ Accuracy: {results['crop_classification']['accuracy']}%")
        
        # Quality Score Model
        if has_quality:
            print("\n📊 Training Quality Score Model...")
            y_quality_train = df.loc[X_train.index, 'quality_score']
            y_quality_test = df.loc[X_test.index, 'quality_score']
            
            self.quality_model = RandomForestRegressor(
                n_estimators=200, max_depth=20, min_samples_split=5,
                min_samples_leaf=2, random_state=42, n_jobs=-1
            )
            self.quality_model.fit(X_train_scaled, y_quality_train)
            y_pred_quality = self.quality_model.predict(X_test_scaled)
            
            rmse = np.sqrt(mean_squared_error(y_quality_test, y_pred_quality))
            r2 = r2_score(y_quality_test, y_pred_quality)
            
            results['quality_score'] = {
                'rmse': round(rmse, 2),
                'r2_score': round(r2, 4),
                'accuracy_percentage': round((1 - rmse/100) * 100, 2)
            }
            print(f"   ✅ RMSE: {rmse:.2f}, R²: {r2:.4f}")
        
        # Yield Estimation Model
        if has_yield:
            print("\n🌾 Training Yield Estimation Model...")
            y_yield_train = df.loc[X_train.index, 'yield_estimation']
            y_yield_test = df.loc[X_test.index, 'yield_estimation']
            
            self.yield_model = RandomForestRegressor(
                n_estimators=200, max_depth=20, min_samples_split=5,
                min_samples_leaf=2, random_state=42, n_jobs=-1
            )
            self.yield_model.fit(X_train_scaled, y_yield_train)
            y_pred_yield = self.yield_model.predict(X_test_scaled)
            
            rmse = np.sqrt(mean_squared_error(y_yield_test, y_pred_yield))
            r2 = r2_score(y_yield_test, y_pred_yield)
            
            results['yield_estimation'] = {
                'rmse': round(rmse, 2),
                'r2_score': round(r2, 4),
                'mean_yield': round(y_yield_train.mean(), 2)
            }
            print(f"   ✅ RMSE: {rmse:.2f}, R²: {r2:.4f}")
        
        # Growth Duration Model
        if has_duration:
            print("\n⏱️ Training Growth Duration Model...")
            y_duration_train = df.loc[X_train.index, 'growth_duration']
            y_duration_test = df.loc[X_test.index, 'growth_duration']
            
            self.duration_model = RandomForestRegressor(
                n_estimators=200, max_depth=20, min_samples_split=5,
                min_samples_leaf=2, random_state=42, n_jobs=-1
            )
            self.duration_model.fit(X_train_scaled, y_duration_train)
            y_pred_duration = self.duration_model.predict(X_test_scaled)
            
            rmse = np.sqrt(mean_squared_error(y_duration_test, y_pred_duration))
            r2 = r2_score(y_duration_test, y_pred_duration)
            
            results['growth_duration'] = {
                'rmse': round(rmse, 2),
                'r2_score': round(r2, 4),
                'mean_duration': round(y_duration_train.mean(), 1)
            }
            print(f"   ✅ RMSE: {rmse:.2f} days, R²: {r2:.4f}")
        
        results['test_samples'] = len(X_test)
        results['train_samples'] = len(X_train)
        
        self.save_model()
        return results
    
    def predict(self, input_data):
        """Predict crop and all metrics"""
        if self.classifier_model is None:
            raise ValueError("Model not trained")
        
        features = np.array([[
            input_data['nitrogen'],
            input_data['phosphorus'],
            input_data['potassium'],
            input_data['temperature'],
            input_data['humidity'],
            input_data['ph'],
            input_data['rainfall']
        ]])
        
        features_scaled = self.scaler.transform(features)
        
        prediction = self.classifier_model.predict(features_scaled)[0]
        probabilities = self.classifier_model.predict_proba(features_scaled)[0]
        
        top_indices = np.argsort(probabilities)[-5:][::-1]
        top_crops = self.classifier_model.classes_[top_indices]
        top_probs = probabilities[top_indices]
        
        recommendations = [
            {
                'crop': crop,
                'confidence': round(prob * 100, 2),
                'suitability': self._get_suitability_label(prob * 100)
            }
            for crop, prob in zip(top_crops, top_probs)
        ]
        
        result = {
            'recommended_crop': prediction,
            'confidence': round(max(probabilities) * 100, 2),
            'all_recommendations': recommendations,
            'feature_contribution': self._analyze_feature_contribution(features[0])
        }
        
        if self.quality_model:
            result['quality_score'] = round(self.quality_model.predict(features_scaled)[0], 2)
            result['quality_grade'] = self._get_quality_grade(result['quality_score'])
        
        if self.yield_model:
            result['yield_estimation'] = round(self.yield_model.predict(features_scaled)[0], 2)
            result['yield_unit'] = 'tonnes/hectare'
        
        if self.duration_model:
            result['growth_duration'] = round(self.duration_model.predict(features_scaled)[0], 1)
            result['duration_unit'] = 'days'
        
        return result
    
    def _get_suitability_label(self, score):
        if score >= 80: return 'Excellent'
        elif score >= 60: return 'Good'
        elif score >= 40: return 'Fair'
        elif score >= 20: return 'Poor'
        else: return 'Not Suitable'
    
    def _get_quality_grade(self, score):
        if score >= 85: return 'Excellent'
        elif score >= 70: return 'Good'
        elif score >= 55: return 'Average'
        else: return 'Poor'
    
    def _analyze_feature_contribution(self, features):
        feature_importance = self.classifier_model.feature_importances_
        contributions = []
        for i, (name, importance) in enumerate(zip(self.feature_names, feature_importance)):
            contributions.append({
                'feature': name,
                'value': features[i],
                'importance': round(importance * 100, 2)
            })
        return sorted(contributions, key=lambda x: x['importance'], reverse=True)
    
    def save_model(self):
        model_data = {
            'classifier_model': self.classifier_model,
            'quality_model': self.quality_model,
            'yield_model': self.yield_model,
            'duration_model': self.duration_model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self):
        if not os.path.exists(self.model_path):
            return False
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            self.classifier_model = model_data['classifier_model']
            self.quality_model = model_data.get('quality_model')
            self.yield_model = model_data.get('yield_model')
            self.duration_model = model_data.get('duration_model')
            self.scaler = model_data['scaler']
            self.feature_names = model_data['feature_names']
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False