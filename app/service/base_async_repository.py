from core import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.service.base_repository import BaseRepository, ModelType
from core.exception import RepositoryInputError

logger = logger.get_logger(__name__)


class BaseAsyncRepository(BaseRepository):
    """Base asynchronous repository with common CRUD operations."""

    def __init__(self, database_session: AsyncSession):
        self._db = database_session

    async def _save_entity(self, entity: ModelType) -> ModelType:
        """Saves a single entity asynchronously."""
        self._validate_entity_not_none(entity)
        entity_name = type(entity).__name__
        try:
            self._db.add(entity)
            await self._db.flush()
            logger.debug(f"Saved {entity_name} id={getattr(entity, 'id', None)}")
            return entity
        except RepositoryInputError:
            raise
        except IntegrityError as error:
            self._handle_integrity_error(entity_name, error)
        except UnmappedInstanceError as error:
            self._handle_unmapped_error(entity_name, error)
        except Exception as error:
            self._handle_generic_error("save", entity_name, error)

    async def _bulk_save_entities(self, entities: list[ModelType]) -> list[ModelType]:
        """Saves multiple entities asynchronously."""
        if not entities:
            logger.debug("No entities to save, skipping bulk save")
            return []
        self._validate_entities_not_none(entities)
        entity_name = type(entities[0]).__name__
        try:
            for entity in entities:
                self._db.add(entity)
            await self._db.flush()
            logger.debug(f"Bulk saved {len(entities)} {entity_name} entities")
            return entities
        except RepositoryInputError:
            raise
        except IntegrityError as error:
            self._handle_integrity_error(entity_name, error)
        except UnmappedInstanceError as error:
            self._handle_unmapped_error(entity_name, error)
        except Exception as error:
            await self._db.rollback()
            self._handle_generic_error("bulk save", entity_name, error)

    async def commit(self) -> None:
        """Commits the current transaction."""
        await self._db.commit()

    async def rollback(self) -> None:
        """Rolls back the current transaction."""
        await self._db.rollback()

    async def close(self) -> None:
        """Closes the database session."""
        await self._db.close()