from typing import List, Dict, Any

class RightsizingEngine:
    def identify_rightsizing_options(self, resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluate resource metrics (e.g. CPU average < 5% implies rightsizing is possible)."""
        recommendations = []
        for res in resources:
            avg_cpu = res.get("cpu_avg", 100.0)
            res_id = res.get("id", "")
            current_size = res.get("size", "t3.large")
            
            if avg_cpu < 5.0:
                recommendations.append({
                    "resource_id": res_id,
                    "reason": "Average CPU utilization under 5% over 7 days.",
                    "action": f"Downsize {current_size} to t3.small.",
                    "monthly_savings_est": 25.0
                })
            elif avg_cpu < 15.0:
                recommendations.append({
                    "resource_id": res_id,
                    "reason": "Average CPU utilization under 15%.",
                    "action": f"Downsize {current_size} to t3.medium.",
                    "monthly_savings_est": 12.0
                })
        return recommendations

# Global rightsizing instance
rightsizing_engine = RightsizingEngine()
