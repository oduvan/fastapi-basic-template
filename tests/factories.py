"""Model factories for testing."""

import factory
from factory import Faker

from app.models.item import Item


class AsyncSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base factory for async SQLAlchemy models."""

    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"


class ItemFactory(AsyncSQLAlchemyModelFactory):
    """Factory for Item model."""

    class Meta:
        model = Item

    title = Faker("sentence", nb_words=4)
    description = Faker("text", max_nb_chars=200)
    is_active = True
