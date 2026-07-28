from typing import List, Dict, Any
from app.services.integration.interface import BaseCloudAdapter

class AWSCloudAdapter(BaseCloudAdapter):
    def get_provider_name(self) -> str:
        return "aws"

    async def discover_resources(self, credentials_json: dict) -> List[Dict[str, Any]]:
        """Mock querying AWS endpoints for EC2, RDS, and EKS details."""
        # Standard production mock
        return [
            {
                "resource_arn": "arn:aws:ec2:us-east-1:123456789012:instance/i-0abc123def456ghi",
                "resource_name": "aegisops-web-server",
                "resource_type": "ec2",
                "region": "us-east-1",
                "metadata": {"instance_size": "t3.medium", "status": "running"}
            },
            {
                "resource_arn": "arn:aws:rds:us-east-1:123456789012:db:aegisops-prod-db",
                "resource_name": "aegisops-db",
                "resource_type": "rds",
                "region": "us-east-1",
                "metadata": {"engine": "postgres", "size": "db.m5.large"}
            },
            {
                "resource_arn": "arn:aws:eks:us-east-1:123456789012:cluster/aegisops-eks",
                "resource_name": "aegisops-kubernetes",
                "resource_type": "EKS",
                "region": "us-east-1",
                "metadata": {"version": "1.29", "node_count": 5}
            }
        ]
