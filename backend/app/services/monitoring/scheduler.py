import asyncio
import logging
from datetime import datetime, timezone
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.metric import DbMetric, DbMetricSnapshot
from app.services.monitoring.local import LocalCollector
from app.services.monitoring.manager import telemetry_broker

logger = logging.getLogger("app.services.monitoring.scheduler")

class MonitoringScheduler:
    def __init__(self) -> None:
        self.collector = LocalCollector()
        self.is_running = False
        self._task = None

    def start(self) -> None:
        if not self.is_running:
            self.is_running = True
            self._task = asyncio.create_task(self._run_loop())
            logger.info("Monitoring metrics scheduler loop started successfully.")

    def stop(self) -> None:
        if self.is_running:
            self.is_running = False
            if self._task:
                self._task.cancel()
            logger.info("Monitoring metrics scheduler loop stopped.")

    async def _run_loop(self) -> None:
        while self.is_running:
            try:
                # Scrape metrics
                metrics = await self.collector.collect_metrics()
                timestamp = datetime.now(timezone.utc)
                
                # Persist snapshot values to database
                async with TestingSessionLocal() as session:
                    for name, value in metrics.items():
                        # Find or create metric entry definition
                        from sqlalchemy import select
                        res = await session.execute(select(DbMetric).where(DbMetric.name == name))
                        metric_def = res.scalar_one_or_none()
                        
                        if not metric_def:
                            metric_def = DbMetric(name=name, unit="%")
                            session.add(metric_def)
                            await session.flush()
                        
                        snapshot = DbMetricSnapshot(
                            metric_id=metric_def.id,
                            target_id="local_host",
                            value=value,
                            timestamp=timestamp
                        )
                        session.add(snapshot)
                    await session.commit()
                
                # Broadcast live updates to subscribers
                await telemetry_broker.broadcast_metric_update(
                    "local_host",
                    {
                        "target_id": "local_host",
                        "timestamp": timestamp.isoformat(),
                        "metrics": metrics
                    }
                )
                
                # Run threshold checking evaluator hook
                from app.services.incident.evaluator import alert_evaluator
                await alert_evaluator.evaluate_metrics("local_host", metrics)
                
            except asyncio.CancelledError:
                break
            except Exception as err:
                logger.error(f"Error in metrics collection cycle: {str(err)}")
            
            await asyncio.sleep(15)  # 15s collection interval

# Global scheduler instance
monitoring_scheduler = MonitoringScheduler()
