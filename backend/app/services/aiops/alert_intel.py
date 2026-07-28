import logging
from typing import List, Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.aiops import DbAlertCluster

logger = logging.getLogger("app.services.aiops.alert_intel")

class AlertIntelligenceEngine:
    async def cluster_alerts(self, incidents: List[Dict[str, Any]]) -> DbAlertCluster:
        """Group incidents sharing matching keyword sets to suppress alert noise."""
        if not incidents:
            return DbAlertCluster(name="Empty Cluster", incident_ids_list={"ids": []}, reduction_ratio=0.0)
            
        # Simple clustering: group by metric name keyword
        groups: Dict[str, List[str]] = {}
        for inc in incidents:
            title = inc.get("title", "")
            inc_id = inc.get("id", "")
            
            # Find a categorizing keyword
            found_key = "generic_alerts"
            for word in ["cpu", "memory", "disk", "database", "network"]:
                if word in title.lower():
                    found_key = f"{word}_anomaly"
                    break
            
            if found_key not in groups:
                groups[found_key] = []
            groups[found_key].append(str(inc_id))
            
        # Pick the largest group to persist as active cluster
        largest_key = max(groups.keys(), key=lambda k: len(groups[k]))
        largest_ids = groups[largest_key]
        
        reduction = 0.0
        if len(incidents) > 1:
            reduction = float((len(incidents) - len(groups)) / len(incidents) * 100.0)
            
        async with TestingSessionLocal() as session:
            cluster = DbAlertCluster(
                name=f"Automated Alert Cluster: {largest_key}",
                incident_ids_list={"ids": largest_ids},
                reduction_ratio=reduction
            )
            session.add(cluster)
            await session.commit()
            return cluster

# Global alert intelligence instance
alert_intel_engine = AlertIntelligenceEngine()
