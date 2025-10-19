"""
Data handling utilities - COMPLETE VERSION
"""
import pandas as pd
import os
from datetime import datetime

class DataHandler:
    """Handle data persistence"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, 'historical_data.csv')
        self.dataset_file = os.path.join(data_dir, 'crop_recommendation.csv')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_prediction(self, prediction, input_data):
        """Save prediction to history"""
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'crop': input_data['crop_type'],
            'nitrogen': input_data.get('nitrogen') or input_data.get('N', 0),
            'phosphorus': input_data.get('phosphorus') or input_data.get('P', 0),
            'potassium': input_data.get('potassium') or input_data.get('K', 0),
            'temperature': input_data['temperature'],
            'humidity': input_data['humidity'],
            'ph': input_data['ph'],
            'rainfall': input_data['rainfall'],
            'score': prediction['score'],
            'quality': prediction['quality'],
            'estimated_yield': prediction['estimated_yield']
        }
        
        if 'growth_duration' in prediction:
            record['growth_duration'] = prediction['growth_duration']
        
        if os.path.exists(self.history_file):
            df = pd.read_csv(self.history_file)
            df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        else:
            df = pd.DataFrame([record])
        
        df.to_csv(self.history_file, index=False)
        return record
    
    def load_history(self, limit=100):
        """Load prediction history"""
        if os.path.exists(self.history_file):
            df = pd.read_csv(self.history_file)
            return df.tail(limit)
        return None
    
    def clear_history(self):
        """Clear all historical data"""
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
            return True
        return False
    
    def export_to_excel(self, filename='crop_predictions_export.xlsx'):
        """Export history to Excel"""
        df = self.load_history()
        if df is not None:
            export_path = os.path.join(self.data_dir, filename)
            df.to_excel(export_path, index=False)
            return export_path
        return None
    
    def get_statistics(self):
        """Get statistical summary"""
        df = self.load_history()
        
        if df is None or df.empty:
            return None
        
        stats = {
            'total_predictions': len(df),
            'crops_analyzed': df['crop'].nunique(),
            'average_score': round(df['score'].mean(), 2),
            'average_yield': round(df['estimated_yield'].mean(), 2),
            'quality_distribution': df['quality'].value_counts().to_dict(),
            'crop_distribution': df['crop'].value_counts().to_dict(),
            'best_prediction': {
                'score': df['score'].max(),
                'crop': df.loc[df['score'].idxmax(), 'crop'],
                'date': df.loc[df['score'].idxmax(), 'timestamp']
            },
            'worst_prediction': {
                'score': df['score'].min(),
                'crop': df.loc[df['score'].idxmin(), 'crop'],
                'date': df.loc[df['score'].idxmin(), 'timestamp']
            }
        }
        
        if 'growth_duration' in df.columns and not df['growth_duration'].isna().all():
            stats['average_growth_duration'] = round(df['growth_duration'].mean(), 1)
        
        return stats


# Convenience functions
def save_to_history(prediction, input_data):
    handler = DataHandler()
    return handler.save_prediction(prediction, input_data)

def load_history(limit=100):
    handler = DataHandler()
    return handler.load_history(limit)

def get_statistics():
    handler = DataHandler()
    return handler.get_statistics()

def export_data(filename='export.xlsx'):
    handler = DataHandler()
    return handler.export_to_excel(filename)