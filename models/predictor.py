"""
Crop Quality Prediction Model - HYBRID VERSION
"""
import numpy as np
from config.settings import CROP_PARAMETERS, ALERT_THRESHOLDS

class CropPredictor:
    """Hybrid crop quality predictor"""
    
    def __init__(self, use_ml=True):
        self.crop_params = CROP_PARAMETERS
        self.alerts = ALERT_THRESHOLDS
        self.use_ml = use_ml
        self.ml_predictor = None
        
        if use_ml:
            try:
                from models.ml_predictor import MLCropPredictor
                self.ml_predictor = MLCropPredictor()
                if self.ml_predictor.classifier_model is None:
                    print("⚠️ ML model not trained. Using rule-based predictions.")
                    self.ml_predictor = None
            except Exception as e:
                print(f"⚠️ Could not load ML model: {e}")
                self.ml_predictor = None
    
    def predict(self, input_data):
        """Predict crop quality"""
        normalized_input = self._normalize_input(input_data)
        crop_type = normalized_input['crop_type']
        
        # Try ML prediction first
        if self.ml_predictor is not None:
            try:
                ml_result = self.ml_predictor.predict({
                    'nitrogen': normalized_input['N'],
                    'phosphorus': normalized_input['P'],
                    'potassium': normalized_input['K'],
                    'temperature': normalized_input['temperature'],
                    'humidity': normalized_input['humidity'],
                    'ph': normalized_input['ph'],
                    'rainfall': normalized_input['rainfall']
                })
                
                if 'quality_score' in ml_result:
                    score = ml_result['quality_score']
                    quality = ml_result.get('quality_grade', self._score_to_quality(score))
                else:
                    score, quality = self._rule_based_score(normalized_input, crop_type)
                
                if 'yield_estimation' in ml_result:
                    estimated_yield = ml_result['yield_estimation']
                else:
                    estimated_yield = self._estimate_yield_from_score(score)
                
                if 'growth_duration' in ml_result:
                    growth_duration = ml_result['growth_duration']
                else:
                    growth_duration = None
                
            except Exception as e:
                print(f"⚠️ ML prediction failed: {e}")
                score, quality = self._rule_based_score(normalized_input, crop_type)
                estimated_yield = self._estimate_yield_from_score(score)
                growth_duration = None
        else:
            score, quality = self._rule_based_score(normalized_input, crop_type)
            estimated_yield = self._estimate_yield_from_score(score)
            growth_duration = None
        
        factors = self._calculate_factors(normalized_input, crop_type)
        recommendations = self._generate_recommendations(factors, crop_type, normalized_input)
        yield_percentage = score * 0.8 + np.random.uniform(5, 20)
        
        result = {
            'score': round(score, 1),
            'quality': quality,
            'factors': factors,
            'recommendations': recommendations,
            'yield_percentage': round(yield_percentage, 1),
            'estimated_yield': round(estimated_yield, 2)
        }
        
        if growth_duration is not None:
            result['growth_duration'] = round(growth_duration, 1)
            result['growth_duration_unit'] = 'days'
        
        return result
    
    def _normalize_input(self, input_data):
        """Normalize input keys"""
        normalized = {}
        normalized['N'] = input_data.get('N') or input_data.get('nitrogen', 0)
        normalized['P'] = input_data.get('P') or input_data.get('phosphorus', 0)
        normalized['K'] = input_data.get('K') or input_data.get('potassium', 0)
        normalized['temperature'] = input_data.get('temperature', 25)
        normalized['humidity'] = input_data.get('humidity', 65)
        normalized['ph'] = input_data.get('ph', 6.5)
        normalized['rainfall'] = input_data.get('rainfall', 100)
        normalized['crop_type'] = input_data.get('crop_type', 'wheat')
        return normalized
    
    def _rule_based_score(self, input_data, crop_type):
        """Calculate score using rule-based approach"""
        optimal = self.crop_params[crop_type]
        
        total_score = 0
        weights = {
            'nitrogen': 0.20, 'phosphorus': 0.15, 'potassium': 0.15,
            'temperature': 0.15, 'humidity': 0.15, 'ph': 0.10, 'rainfall': 0.10
        }
        
        n_score = max(0, 100 - abs(input_data['N'] - optimal['nitrogen']) * 0.8)
        total_score += n_score * weights['nitrogen']
        
        p_score = max(0, 100 - abs(input_data['P'] - optimal['phosphorus']) * 1.5)
        total_score += p_score * weights['phosphorus']
        
        k_score = max(0, 100 - abs(input_data['K'] - optimal['potassium']) * 1.5)
        total_score += k_score * weights['potassium']
        
        temp_score = max(0, 100 - abs(input_data['temperature'] - optimal['temperature']) * 3)
        total_score += temp_score * weights['temperature']
        
        hum_optimal = optimal['humidity']
        if 40 <= input_data['humidity'] <= 80:
            hum_score = 100 - abs(input_data['humidity'] - hum_optimal) * 1.5
        else:
            hum_score = max(0, 50 - abs(input_data['humidity'] - hum_optimal) * 2)
        total_score += hum_score * weights['humidity']
        
        if 6.0 <= input_data['ph'] <= 7.5:
            ph_score = 100 - abs(input_data['ph'] - optimal['ph']) * 20
        else:
            ph_score = max(0, 60 - abs(input_data['ph'] - optimal['ph']) * 25)
        total_score += ph_score * weights['ph']
        
        rain_score = max(0, 100 - abs(input_data['rainfall'] - optimal['rainfall']) * 0.5)
        total_score += rain_score * weights['rainfall']
        
        quality = self._score_to_quality(total_score)
        return total_score, quality
    
    def _score_to_quality(self, score):
        if score >= 80: return 'Excellent'
        elif score >= 65: return 'Good'
        elif score >= 50: return 'Average'
        else: return 'Poor'
    
    def _estimate_yield_from_score(self, score):
        yield_percentage = score * 0.8 + np.random.uniform(5, 20)
        return (yield_percentage / 100) * 4.5
    
    def _calculate_factors(self, input_data, crop_type):
        """Calculate individual factor scores"""
        optimal = self.crop_params[crop_type]
        factors = []
        
        n_score = max(0, 100 - abs(input_data['N'] - optimal['nitrogen']) * 0.8)
        factors.append({'name': 'Nitrogen', 'score': round(n_score, 1),
                       'current': input_data['N'], 'optimal': optimal['nitrogen']})
        
        p_score = max(0, 100 - abs(input_data['P'] - optimal['phosphorus']) * 1.5)
        factors.append({'name': 'Phosphorus', 'score': round(p_score, 1),
                       'current': input_data['P'], 'optimal': optimal['phosphorus']})
        
        k_score = max(0, 100 - abs(input_data['K'] - optimal['potassium']) * 1.5)
        factors.append({'name': 'Potassium', 'score': round(k_score, 1),
                       'current': input_data['K'], 'optimal': optimal['potassium']})
        
        temp_score = max(0, 100 - abs(input_data['temperature'] - optimal['temperature']) * 3)
        factors.append({'name': 'Temperature', 'score': round(temp_score, 1),
                       'current': input_data['temperature'], 'optimal': optimal['temperature']})
        
        hum_optimal = optimal['humidity']
        if 40 <= input_data['humidity'] <= 80:
            hum_score = 100 - abs(input_data['humidity'] - hum_optimal) * 1.5
        else:
            hum_score = max(0, 50 - abs(input_data['humidity'] - hum_optimal) * 2)
        factors.append({'name': 'Humidity', 'score': round(hum_score, 1),
                       'current': input_data['humidity'], 'optimal': hum_optimal})
        
        if 6.0 <= input_data['ph'] <= 7.5:
            ph_score = 100 - abs(input_data['ph'] - optimal['ph']) * 20
        else:
            ph_score = max(0, 60 - abs(input_data['ph'] - optimal['ph']) * 25)
        factors.append({'name': 'pH Level', 'score': round(ph_score, 1),
                       'current': input_data['ph'], 'optimal': optimal['ph']})
        
        rain_score = max(0, 100 - abs(input_data['rainfall'] - optimal['rainfall']) * 0.5)
        factors.append({'name': 'Rainfall', 'score': round(rain_score, 1),
                       'current': input_data['rainfall'], 'optimal': optimal['rainfall']})
        
        return factors
    
    def _generate_recommendations(self, factors, crop_type, input_data):
        """Generate recommendations"""
        recommendations = []
        
        for factor in factors:
            if factor['score'] < 70:
                if factor['name'] == 'Nitrogen':
                    recommendations.append(f"⚠️ Nitrogen: Adjust from {factor['current']} to ~{factor['optimal']} kg/ha")
                elif factor['name'] == 'Phosphorus':
                    recommendations.append(f"⚠️ Phosphorus: Increase to {factor['optimal']} kg/ha (current: {factor['current']})")
                elif factor['name'] == 'Potassium':
                    recommendations.append(f"⚠️ Potassium: Increase to {factor['optimal']} kg/ha (current: {factor['current']})")
                elif factor['name'] == 'Temperature':
                    recommendations.append(f"🌡️ Temperature: {factor['current']}°C not optimal for {crop_type} (optimal: {factor['optimal']}°C)")
                elif factor['name'] == 'Humidity':
                    recommendations.append(f"💧 Humidity: Adjust to {factor['optimal']}% (current: {factor['current']}%)")
                elif factor['name'] == 'pH Level':
                    recommendations.append(f"🧪 Soil pH: Needs correction from {factor['current']} to {factor['optimal']}")
                elif factor['name'] == 'Rainfall':
                    recommendations.append(f"🌧️ Rainfall: Adjust irrigation (current: {factor['current']}mm, optimal: {factor['optimal']}mm)")
        
        if not recommendations:
            recommendations.append("✅ All parameters are optimal! Maintain current practices.")
        
        return recommendations
    
    def generate_alerts(self, nitrogen, phosphorus, potassium, temperature, 
                       humidity, ph, rainfall):
        """Generate alerts for critical conditions"""
        alerts = []
        
        if ph < self.alerts['ph_min'] or ph > self.alerts['ph_max']:
            alerts.append({
                'type': 'critical',
                'message': f'pH level {ph} is outside safe range ({self.alerts["ph_min"]}-{self.alerts["ph_max"]})'
            })
        
        if nitrogen < self.alerts['nitrogen_min']:
            alerts.append({
                'type': 'warning',
                'message': f'Nitrogen levels are low ({nitrogen} kg/ha). Consider fertilizer application'
            })
        
        if temperature > self.alerts['temperature_max']:
            alerts.append({
                'type': 'critical',
                'message': f'Temperature {temperature}°C is too high! Risk of crop stress'
            })
        
        if humidity < self.alerts['humidity_min']:
            alerts.append({
                'type': 'warning',
                'message': f'Low humidity detected ({humidity}%). Increase irrigation'
            })
        
        if rainfall < self.alerts['rainfall_min']:
            alerts.append({
                'type': 'warning',
                'message': f'Insufficient rainfall ({rainfall}mm). Plan for irrigation'
            })
        
        return alerts