from core import logger
from typing import TypeVar
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from core.exception import RepositoryInputError, ServiceRepositoryError

logger = logger.get_logger(__name__)
ModelType = TypeVar("ModelType")


class BaseRepository:
    """Common logic for both synchronous and asynchronous repositories."""

    def _validate_entity_not_none(self, entity: ModelType) -> None:
        """Validates that the entity is not None."""
        if entity is None:
            raise RepositoryInputError("Entity cannot be None")

    def _validate_entities_not_none(self, entities: list[ModelType]) -> None:
        """Validates that all entities in the list are not None."""
        for entity in entities:
            if entity is None:
                raise RepositoryInputError("Entity in list cannot be None")

    def _handle_integrity_error(self, entity_name: str, error: IntegrityError) -> None:
        """Handles database integrity errors."""
        logger.error(f"Integrity error for {entity_name}: {error}")
        raise ServiceRepositoryError(f"Database integrity error for {entity_name}") from error

    def _handle_unmapped_error(self, entity_name: str, error: UnmappedInstanceError) -> None:
        """Handles unmapped instance errors (wrong entity type)."""
        logger.error(f"Invalid entity type: {entity_name} - {error}")
        raise RepositoryInputError(f"Invalid entity type: {entity_name}") from error

    def _handle_generic_error(self, operation: str, entity_name: str, error: Exception) -> None:
        """Handles any other unexpected errors."""
        logger.error(f"Failed to {operation} {entity_name}: {error}")
        raise ServiceRepositoryError(f"Failed to {operation} {entity_name}: {error}") from error