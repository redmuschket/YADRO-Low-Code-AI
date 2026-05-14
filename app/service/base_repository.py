import logging
from typing import TypeVar
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from core.exception import RepositoryInputError, ServiceRepositoryError

logger = logging.getLogger(__name__)
ModelType = TypeVar("ModelType")


class BaseRepository:
    """Common logic for synchronous and asynchronous repositories."""

    def _save_entity(self, entity: ModelType) -> ModelType:
        if entity is None:
            raise RepositoryInputError("Entity cannot be None")
        try:
            self._db.add(entity)
            self._flush()
            logger.debug(f"Saved {type(entity).__name__} id={getattr(entity, 'id', None)}")
            return entity
        except RepositoryInputError:
            raise
        except IntegrityError as e:
            logger.error(f"Integrity error saving {type(entity).__name__}: {e}")
            raise ServiceRepositoryError("Database integrity error") from e
        except UnmappedInstanceError as e:
            logger.error(f"Invalid entity type: {type(entity).__name__} - {e}")
            raise RepositoryInputError(f"Invalid entity type: {type(entity).__name__}") from e
        except Exception as e:
            logger.error(f"Failed to save {type(entity).__name__}: {e}")
            raise ServiceRepositoryError(f"Failed to save {type(entity).__name__}: {e}")

    def _bulk_save_entities(self, entities: list[ModelType]) -> list[ModelType]:
        if not entities:
            return []
        entity_name = type(entities[0]).__name__
        try:
            for entity in entities:
                if entity is None:
                    raise RepositoryInputError("Entity in list cannot be None")
                self._db.add(entity)
            self._flush()
            logger.debug(f"Bulk saved {len(entities)} {entity_name} entities")
            return entities
        except RepositoryInputError:
            raise
        except IntegrityError as e:
            logger.error(f"Integrity error bulk saving {entity_name}: {e}")
            raise ServiceRepositoryError(f"Database integrity error for {entity_name}") from e
        except UnmappedInstanceError as e:
            logger.error(f"Invalid entity type in bulk save: {entity_name} - {e}")
            raise RepositoryInputError(f"Invalid entity type: {entity_name}") from e
        except Exception as e:
            logger.error(f"Bulk save failed for {entity_name}: {e}")
            raise ServiceRepositoryError(f"Bulk save failed for {entity_name}: {e}") from e

    def _flush(self):
        """Redefined in the heirs."""
        raise NotImplementedError
