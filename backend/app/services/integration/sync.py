import json
import logging
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.integration import DbIntegrationAccount, DbCloudResource, DbSyncLog
from app.services.integration.adapters.aws import AWSCloudAdapter

logger = logging.getLogger("app.services.integration.sync")

class InventorySynchronizationEngine:
    def __init__(self) -> None:
        self.aws_adapter = AWSCloudAdapter()

    async def synchronize_account_inventory(self, account_id: str) -> bool:
        """Query adapters for target accounts, parsing resources and updating database caches."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            import uuid
            res = await session.execute(
                select(DbIntegrationAccount).where(DbIntegrationAccount.id == uuid.UUID(account_id))
            )
            account = res.scalar_one_or_none()
            if not account:
                return False

            account.sync_status = "synchronizing"
            session.add(account)
            await session.commit()

            try:
                # Discovered resources mock lists
                resources = await self.aws_adapter.discover_resources({})
                
                # Fetch existing resource lists to avoid duplicates
                res_exist = await session.execute(
                    select(DbCloudResource).where(DbCloudResource.account_id == account.id)
                )
                existing_map = {r.resource_arn: r for r in res_exist.scalars().all()}
                
                for r in resources:
                    arn = r["resource_arn"]
                    if arn in existing_map:
                        db_res = existing_map[arn]
                        db_res.resource_name = r["resource_name"]
                        db_res.metadata_json = r["metadata"]
                    else:
                        db_res = DbCloudResource(
                            account_id=account.id,
                            resource_arn=arn,
                            resource_name=r["resource_name"],
                            resource_type=r["resource_type"],
                            region=r["region"],
                            metadata_json=r["metadata"]
                        )
                    session.add(db_res)
                
                # Audit log
                sync_log = DbSyncLog(
                    account_id=account.id,
                    status="success",
                    message=f"Discovered and synchronized {len(resources)} cloud resources."
                )
                session.add(sync_log)
                
                account.sync_status = "idle"
                session.add(account)
                await session.commit()
                return True
                
            except Exception as err:
                logger.error(f"Failed to synchronize integration account resources: {str(err)}")
                account.sync_status = "failed"
                session.add(account)
                
                sync_log = DbSyncLog(
                    account_id=account.id,
                    status="failed",
                    message=f"Sync execution failed: {str(err)}"
                )
                session.add(sync_log)
                await session.commit()
                return False

# Global sync engine instance
inventory_synchronizer = InventorySynchronizationEngine()

# Synchronization stubs cleaned
