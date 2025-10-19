"""
Calculators for Fertilizer, Irrigation, and Profit Analysis
Enhanced with exact timeline design from specifications
"""
from config.settings import CROP_PARAMETERS, FERTILIZER_PRICES

class FertilizerCalculator:
    """Calculate fertilizer requirements and costs"""
    
    def __init__(self):
        self.crop_params = CROP_PARAMETERS
        self.prices = FERTILIZER_PRICES
    
    def calculate(self, crop_type, current_n, current_p, current_k):
        """
        Calculate fertilizer needs
        
        Returns:
        --------
        dict : Required, current, deficit NPK values and total cost
        """
        required = self.crop_params[crop_type]
        
        deficit_n = max(0, required['nitrogen'] - current_n)
        deficit_p = max(0, required['phosphorus'] - current_p)
        deficit_k = max(0, required['potassium'] - current_k)
        
        total_cost = (
            deficit_n * self.prices['nitrogen'] +
            deficit_p * self.prices['phosphorus'] +
            deficit_k * self.prices['potassium']
        )
        
        return {
            'required': {
                'N': required['nitrogen'],
                'P': required['phosphorus'],
                'K': required['potassium']
            },
            'current': {
                'N': current_n,
                'P': current_p,
                'K': current_k
            },
            'deficit': {
                'N': deficit_n,
                'P': deficit_p,
                'K': deficit_k
            },
            'total_cost': round(total_cost, 2),
            'cost_breakdown': {
                'nitrogen': round(deficit_n * self.prices['nitrogen'], 2),
                'phosphorus': round(deficit_p * self.prices['phosphorus'], 2),
                'potassium': round(deficit_k * self.prices['potassium'], 2)
            }
        }
    
    def get_application_schedule(self):
        """Return enhanced fertilizer application schedule matching the exact design"""
        return [
            {
                'stage': 'STAGE 1',
                'subtitle': 'Base Application',
                'timing': '0 days',
                'timing_detail': 'Before Planting',
                'fertilizer': '50% of total NPK',
                'npk_ratio': '50% N + 100% P + 100% K',
                'description': 'Apply during land preparation to establish nutrient foundation',
                'tips': [
                    'Mix thoroughly with soil',
                    'Apply 2-3 days before sowing',
                    'Ensure proper soil moisture'
                ],
                'icon': '🌱',
                'color': '#10b981',
                'percentage': 50
            },
            {
                'stage': 'STAGE 2',
                'subtitle': 'First Top Dressing',
                'timing': '30 days',
                'timing_detail': '30 days after planting',
                'fertilizer': '25% of Nitrogen',
                'npk_ratio': '25% N only',
                'description': 'Apply during active vegetative growth to boost plant development',
                'tips': [
                    'Apply near root zone',
                    'Water immediately after application',
                    'Avoid direct contact with stems'
                ],
                'icon': '🌿',
                'color': '#3b82f6',
                'percentage': 25
            },
            {
                'stage': 'STAGE 3',
                'subtitle': 'Second Top Dressing',
                'timing': '60 days',
                'timing_detail': '60 days after planting',
                'fertilizer': 'Remaining 25% N',
                'npk_ratio': '25% N only',
                'description': 'Apply during flowering/grain filling stage for optimal yield',
                'tips': [
                    'Apply before flowering begins',
                    'Ensure adequate soil moisture',
                    'Monitor plant response'
                ],
                'icon': '🌾',
                'color': '#f59e0b',
                'percentage': 25
            }
        ]


class IrrigationCalculator:
    """Calculate irrigation requirements"""
    
    def __init__(self):
        self.crop_params = CROP_PARAMETERS
    
    def calculate(self, crop_type, rainfall):
        """
        Calculate irrigation needs
        
        Returns:
        --------
        dict : Water requirements and irrigation schedule
        """
        # Water requirement varies by crop (mm per season)
        water_requirements = {
            'rice': 1200,
            'sugarcane': 1800,
            'wheat': 500,
            'maize': 600,
            'cotton': 700,
            'potato': 500,
            'tomato': 600,
            'soybean': 500
        }
        
        total_needed = water_requirements.get(crop_type, 600)
        rain_contribution = rainfall * 4  # Assuming monthly rainfall for 4 months
        irrigation_needed = max(0, total_needed - rain_contribution)
        
        # Irrigation frequency per week
        frequency_map = {
            'rice': 3,
            'sugarcane': 3,
            'wheat': 2,
            'maize': 2,
            'cotton': 2,
            'potato': 3,
            'tomato': 3,
            'soybean': 2
        }
        
        frequency = frequency_map.get(crop_type, 2)
        
        # Weekly schedule
        schedules = {
            2: ['Monday', 'Thursday'],
            3: ['Monday', 'Wednesday', 'Friday']
        }
        
        schedule = schedules.get(frequency, ['Monday', 'Thursday'])
        
        # Water per irrigation session
        water_per_session = round(irrigation_needed / frequency / 16, 2) if frequency > 0 else 0
        
        return {
            'total_needed': total_needed,
            'rain_contribution': rain_contribution,
            'irrigation_needed': irrigation_needed,
            'frequency': frequency,
            'schedule': schedule,
            'water_per_session': water_per_session,
            'efficiency_percentage': round((rain_contribution / total_needed) * 100, 1)
        }
    
    def get_irrigation_tips(self):
        """Return irrigation best practices"""
        return [
            "💧 Early morning irrigation (6-8 AM) is most efficient",
            "🌡️ Avoid irrigation during peak afternoon heat (12-3 PM)",
            "🌱 Monitor soil moisture before each irrigation",
            "🌧️ Adjust schedule based on rainfall events",
            "💡 Use drip irrigation for water conservation",
            "📊 Check for proper drainage to avoid waterlogging"
        ]


class ProfitCalculator:
    """Calculate profit and ROI"""
    
    def calculate(self, costs, expected_price, estimated_yield):
        """
        Calculate profit analysis
        
        Parameters:
        -----------
        costs : dict
            Contains seed_cost, fertilizer_cost, labor_cost, irrigation_cost
        expected_price : float
            Expected market price per quintal (INR)
        estimated_yield : float
            Expected yield in tonnes per hectare
            
        Returns:
        --------
        dict : Cost, revenue, profit, and ROI analysis
        """
        total_cost = (
            costs['seed_cost'] +
            costs['fertilizer_cost'] +
            costs['labor_cost'] +
            costs['irrigation_cost']
        )
        
        # Convert tonnes to quintals (1 tonne = 10 quintals)
        yield_quintals = estimated_yield * 10
        
        # Calculate revenue
        revenue = yield_quintals * expected_price
        
        # Calculate profit
        profit = revenue - total_cost
        
        # Calculate ROI
        roi = (profit / total_cost * 100) if total_cost > 0 else 0
        
        # Break-even analysis
        break_even_yield = total_cost / expected_price / 10 if expected_price > 0 else 0
        
        return {
            'total_cost': round(total_cost, 2),
            'revenue': round(revenue, 2),
            'profit': round(profit, 2),
            'roi': round(roi, 2),
            'yield_tonnes': estimated_yield,
            'yield_quintals': round(yield_quintals, 2),
            'break_even_yield': round(break_even_yield, 2),
            'cost_breakdown': {
                'seed': costs['seed_cost'],
                'fertilizer': costs['fertilizer_cost'],
                'labor': costs['labor_cost'],
                'irrigation': costs['irrigation_cost']
            }
        }


# Mock implementations for testing
if __name__ == "__main__":
    # Test the fertilizer calculator
    fert_calc = FertilizerCalculator()
    schedule = fert_calc.get_application_schedule()
    
    print("Fertilizer Application Schedule:")
    for stage in schedule:
        print(f"\n{stage['stage']}: {stage['subtitle']}")
        print(f"Timing: {stage['timing']} ({stage['timing_detail']})")
        print(f"Application: {stage['fertilizer']}")
        print(f"NPK Ratio: {stage['npk_ratio']}")
        print(f"Description: {stage['description']}")
        print("Tips:")
        for tip in stage['tips']:
            print(f"  ✓ {tip}")