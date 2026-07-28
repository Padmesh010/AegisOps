import asyncio
import logging
from typing import Callable, TypeVar, Any
from app.providers.ai.interface import AIProvider
from app.core.exceptions import AIRateLimitError, AIConnectionTimeout, AIProviderError

logger = logging.getLogger("app.providers.ai.base")
T = TypeVar("T")

class BaseProvider(AIProvider):
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0) -> None:
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    async def execute_with_retry(self, func: Callable[[], Any], *args: Any, **kwargs: Any) -> Any:
        """Execute async network calls with exponential backoff on retryable failures."""
        retries = 0
        delay = 1.0
        while True:
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except (AIRateLimitError, AIConnectionTimeout) as err:
                retries += 1
                if retries > self.max_retries:
                    logger.error(f"Provider {self.get_name()} execution failed after {self.max_retries} retries: {str(err)}")
                    raise err
                logger.warn(f"Provider {self.get_name()} failed. Retrying in {delay}s (Attempt {retries}/{self.max_retries}). Error: {str(err)}")
                await asyncio.sleep(delay)
                delay *= self.backoff_factor
            except Exception as err:
                if not isinstance(err, AIProviderError):
                    raise AIProviderError(f"Unexpected provider error: {str(err)}", provider=self.get_name())
                raise err
