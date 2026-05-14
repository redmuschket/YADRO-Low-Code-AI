from core import logger
from core.exceptions import TransactionError, RepositoryInputError, ServiceRepositoryError

from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError
from typing import List, TypeVar, Generic
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from typing import overload, Union
from sqlalchemy.ext.asyncio import AsyncSession

logger = logger.get_logger(__name__)
ModelType = TypeVar("ModelType")


class RepositoryService:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def commit_transaction(self) -> None:
        """Fixing a transaction in the database"""
        try:
            await self._db.commit()
        except Exception as e:
            logger.error(f"Failed to commit transaction: {e}")
            await self.rollback_db()
            raise TransactionError(f"Failed to commit transaction: {e}")

    async def rollback_db(self) -> None:
        """Rollback of a database transaction"""
        try:
            await self._db.rollback()
        except Exception as e:
            logger.error(f"Failed to rollback transaction: {e}")

    async def _save_entity(self, entity: ModelType) -> ModelType:
        """
        The basic method of saving a single entity.
        Performs adding to the session, flush, and error handling.
        """
        try:
            if entity is None:
                raise RepositoryInputError("Entity cannot be None")
            self._db.add(entity)
            await self._db.flush()

            logger.debug(f"Successfully saved {type(entity).__name__} with id={getattr(entity, 'id', None)}")

            return entity
        except RepositoryInputError:
            raise
        except IntegrityError as e:
            logger.error(f"Database integrity error while saving {type(entity).__name__}: {e}")
            raise ServiceRepositoryError(f"Database integrity error") from e
        except UnmappedInstanceError as e:
            logger.error(f"Invalid entity type: {type(entity).__name__} - {e}")
            raise RepositoryInputError(f"Invalid entity type: {type(entity).__name__}") from e
        except Exception as e:
            logger.error(f"Failed to save entity {type(entity).__name__}: {e}")
            raise ServiceRepositoryError(f"Failed to save {type(entity).__name__}: {e}")

    async def _bulk_save_entities(self, entities: list[ModelType]) -> list[ModelType]:
        """
        The basic method for saving a list of entities en masse.
        """

        if not entities:
            logger.debug("No entities to save, skipping bulk save")
            return []

        entity_name = type(entities[0]).__name__

        try:
            for entity in entities:
                if entity is None:
                    raise RepositoryInputError("Entity in list cannot be None")
                self._db.add(entity)
            await self._db.flush()

            logger.debug(f"Successfully bulk saved {len(entities)} {entity_name} entities")

            return entities
        except RepositoryInputError:
            raise
        except IntegrityError as e:
            logger.error(f"Database integrity error while saving {entity_name}: {e}")
            raise ServiceRepositoryError(f"Database integrity error for {entity_name}") from e
        except UnmappedInstanceError as e:
            logger.error(f"Invalid entity type in bulk save: {entity_name} - {e}")
            raise RepositoryInputError(f"Invalid entity type: {entity_name}") from e
        except Exception as e:
            logger.error(f"Failed to bulk save entities {entity_name}: {e}")
            await self._db.rollback()
            raise ServiceRepositoryError(f"Bulk save failed for {entity_name}: {e}") from e