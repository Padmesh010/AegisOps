import psutil
from typing import Dict
from app.services.monitoring.interface import BaseCollector

class LocalCollector(BaseCollector):
    def get_collector_name(self) -> str:
        return "local_system"

    async def collect_metrics(self) -> Dict[str, float]:
        """Collect host system memory, CPU, disk and network rates using psutil."""
        try:
            cpu_pct = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            
            # Simple difference of network bytes (first collection is baseline)
            net = psutil.net_io_counters()
            
            return {
                "cpu_utilization_percent": float(cpu_pct),
                "memory_utilization_percent": float(mem.percent),
                "disk_utilization_percent": float(disk.percent),
                "network_bytes_sent_rate": float(net.bytes_sent),
                "network_bytes_received_rate": float(net.bytes_recv)
            }
        except Exception:
            return {
                "cpu_utilization_percent": 0.0,
                "memory_utilization_percent": 0.0,
                "disk_utilization_percent": 0.0,
                "network_bytes_sent_rate": 0.0,
                "network_bytes_received_rate": 0.0
            }
