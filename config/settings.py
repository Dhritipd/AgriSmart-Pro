"""
Configuration settings for the application
"""

# Crop optimal parameters
CROP_PARAMETERS = {
    'wheat': {
        'nitrogen': 100,
        'phosphorus': 40,
        'potassium': 30,
        'temperature': 22,
        'humidity': 60,
        'ph': 6.5,
        'rainfall': 80
    },
    'rice': {
        'nitrogen': 120,
        'phosphorus': 50,
        'potassium': 40,
        'temperature': 28,
        'humidity': 70,
        'ph': 6.5,
        'rainfall': 150
    },
    'maize': {
        'nitrogen': 100,
        'phosphorus': 45,
        'potassium': 35,
        'temperature': 25,
        'humidity': 65,
        'ph': 6.0,
        'rainfall': 100
    },
    'cotton': {
        'nitrogen': 80,
        'phosphorus': 35,
        'potassium': 30,
        'temperature': 27,
        'humidity': 60,
        'ph': 6.5,
        'rainfall': 90
    },
    'sugarcane': {
        'nitrogen': 150,
        'phosphorus': 60,
        'potassium': 50,
        'temperature': 30,
        'humidity': 75,
        'ph': 6.5,
        'rainfall': 180
    },
    'potato': {
        'nitrogen': 90,
        'phosphorus': 50,
        'potassium': 50,
        'temperature': 20,
        'humidity': 70,
        'ph': 5.5,
        'rainfall': 70
    },
    'tomato': {
        'nitrogen': 100,
        'phosphorus': 50,
        'potassium': 50,
        'temperature': 24,
        'humidity': 65,
        'ph': 6.0,
        'rainfall': 60
    },
    'soybean': {
        'nitrogen': 60,
        'phosphorus': 40,
        'potassium': 40,
        'temperature': 26,
        'humidity': 65,
        'ph': 6.5,
        'rainfall': 120
    }
}

# Regional recommendations
REGIONAL_DATA = {
    'West Bengal': {
        'suitable_crops': ['rice', 'potato', 'wheat'],
        'season': 'Kharif suitable for rice',
        'rainfall_pattern': 'High rainfall region',
        'soil_type': 'Alluvial'
    },
    'Punjab': {
        'suitable_crops': ['wheat', 'rice', 'cotton'],
        'season': 'Best for wheat in Rabi',
        'rainfall_pattern': 'Irrigation dependent',
        'soil_type': 'Alluvial'
    },
    'Maharashtra': {
        'suitable_crops': ['cotton', 'sugarcane', 'soybean'],
        'season': 'Cotton in Kharif',
        'rainfall_pattern': 'Moderate rainfall',
        'soil_type': 'Black soil'
    },
    'Tamil Nadu': {
        'suitable_crops': ['rice', 'sugarcane', 'cotton'],
        'season': 'Rice throughout year',
        'rainfall_pattern': 'Delta irrigation',
        'soil_type': 'Alluvial and Clay'
    },
    'Uttar Pradesh': {
        'suitable_crops': ['wheat', 'rice', 'sugarcane'],
        'season': 'Wheat-Rice rotation',
        'rainfall_pattern': 'Moderate rainfall',
        'soil_type': 'Alluvial'
    },
    'Bihar': {
        'suitable_crops': ['rice', 'wheat', 'maize'],
        'season': 'Rice in Kharif, Wheat in Rabi',
        'rainfall_pattern': 'High rainfall',
        'soil_type': 'Alluvial'
    },
    'Karnataka': {
        'suitable_crops': ['rice', 'cotton', 'sugarcane'],
        'season': 'Multiple cropping seasons',
        'rainfall_pattern': 'Variable rainfall',
        'soil_type': 'Red and Black soil'
    },
    'Gujarat': {
        'suitable_crops': ['cotton', 'wheat', 'potato'],
        'season': 'Cotton in Kharif',
        'rainfall_pattern': 'Low to moderate',
        'soil_type': 'Black and Alluvial'
    },
    'Haryana': {
        'suitable_crops': ['wheat', 'rice', 'cotton'],
        'season': 'Wheat dominant in Rabi',
        'rainfall_pattern': 'Canal irrigation',
        'soil_type': 'Alluvial'
    },
    'Madhya Pradesh': {
        'suitable_crops': ['wheat', 'soybean', 'cotton'],
        'season': 'Soybean in Kharif',
        'rainfall_pattern': 'Moderate rainfall',
        'soil_type': 'Black soil'
    },
    'Rajasthan': {
        'suitable_crops': ['wheat', 'cotton', 'maize'],
        'season': 'Wheat in Rabi',
        'rainfall_pattern': 'Low rainfall - irrigation needed',
        'soil_type': 'Sandy and Alluvial'
    },
    'Andhra Pradesh': {
        'suitable_crops': ['rice', 'cotton', 'sugarcane'],
        'season': 'Rice primary crop',
        'rainfall_pattern': 'Coastal high rainfall',
        'soil_type': 'Alluvial and Red'
    }
}

# Fertilizer prices (INR per kg)
FERTILIZER_PRICES = {
    'nitrogen': 25,
    'phosphorus': 40,
    'potassium': 30
}

# Alert thresholds
ALERT_THRESHOLDS = {
    'ph_min': 5.5,
    'ph_max': 8.0,
    'nitrogen_min': 30,
    'temperature_max': 40,
    'humidity_min': 30,
    'rainfall_min': 30
}

# Color schemes
QUALITY_COLORS = {
    'Excellent': '#10b981',
    'Good': '#3b82f6',
    'Average': '#f59e0b',
    'Poor': '#ef4444'
}