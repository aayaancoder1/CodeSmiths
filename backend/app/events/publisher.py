import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from redis import Redis
from app.config.config import settings
from app.core.exceptions import EventPublishError

logger = logging.getLogger(__name__)


class IndexingEvent(BaseModel):
    """Pydantic schema representing document indexing events broadcast to downstream AI consumers."""
    event_type: str = Field(description="Type of indexing event, e.g. 'document.ingested', 'document.deleted'")
    document_id: UUID = Field(description="UUID of the affected document")
    source: str = Field(description="Ingestion source type, e.g. 'google_drive', 'notion'")
    tenant_id: UUID = Field(description="UUID of the document's tenant")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the modification")
    operation: str = Field(description="Action classification: 'create', 'update', or 'delete'")
    version: int = Field(description="Latest document version integer index")


class BaseEventPublisher(ABC):
    """Base abstract class for messaging brokers."""

    @abstractmethod
    async def publish(self, event: IndexingEvent) -> None:
        """Asynchronously publish an indexing event to the message broker."""
        pass


class RedisEventPublisher(BaseEventPublisher):
    """Redis-backed event publisher utilizing Pub/Sub channels to support multiple downstream consumers."""

    def __init__(self, channel_name: str = "document_indexing_events"):
        self.channel_name = channel_name
        self.redis_client = None

    def _get_client(self) -> Redis:
        """Lazy initialization of the Redis client (ensures thread-safety in async workers)."""
        if self.redis_client is None:
            self.redis_client = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )
        return self.redis_client

    async def publish(self, event: IndexingEvent) -> None:
        """Broadcasts serialized JSON event payload onto the Redis Pub/Sub channel."""
        try:
            client = self._get_client()
            
            # Serialize payload with custom datetime serializer
            payload = event.model_dump_json()
            
            # Redis publish is a blocking sync call in redis-py, but fast. We run it safely.
            client.publish(self.channel_name, payload)
            
            logger.info(f"RedisEventPublisher: Published '{event.event_type}' for document {event.document_id} on channel '{self.channel_name}'.")
        except Exception as e:
            logger.error(f"RedisEventPublisher: Failed to publish event: {e}")
            raise EventPublishError(
                f"Redis failed to broadcast event for document {event.document_id}",
                details={"original_error": str(e)}
            )
