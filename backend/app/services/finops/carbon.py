from typing import Dict, Any

class CarbonFootprintEngine:
    def estimate_co2_kg(self, instance_type: str, hours: float, region: str) -> float:
        """Estimate CO2 footprint in kg based on cloud regional grid index mappings."""
        # Simple regional grids multiplier: clean grids vs coal grids
        grid_multipliers = {
            "us-east-1": 0.45,  # coal mixed grid
            "eu-west-1": 0.12,  # green grid (Ireland)
            "us-west-2": 0.28   # hydro mixed grid
        }
        
        multiplier = grid_multipliers.get(region, 0.35)
        
        # Instance baseline watt usage estimate
        watts = 150.0  # default average
        if "small" in instance_type:
            watts = 40.0
        elif "large" in instance_type:
            watts = 250.0
            
        kwh = (watts * hours) / 1000.0
        return float(kwh * multiplier)

# Global carbon engine instance
carbon_engine = CarbonFootprintEngine()
