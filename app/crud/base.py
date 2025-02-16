import logging
import pydantic

from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from core.models import Base


class BaseDAO[T: Base, V: pydantic.BaseModel]:
    model: type[T]

    @classmethod
    async def create(cls, validated_values: V, session: AsyncSession) -> T:
        instance = cls.model(**validated_values.model_dump())
        session.add(instance)

        try:
            await session.flush()
            await session.commit()
            logging.info(
                "%s successfully created with values: %s",
                cls.model.__name__,
                validated_values,
            )
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error("Error creating %s: %s", cls.model.__name__, e)
            raise

        return instance

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[T]:
        try:
            stmt = select(cls.model)
            result = await session.scalars(stmt)
            instances = result.all()
            return instances
        except SQLAlchemyError as e:
            logging.error("Error fetching all %s: %s", cls.model.__name__, e)

    @classmethod
    async def get_by_id(cls, model_id: int, session: AsyncSession) -> T | None:
        try:
            stmt = select(cls.model).where(cls.model.id == model_id)
            result = await session.scalars(stmt)
            instance = result.one_or_none()
            if instance is None:
                logging.warning("%s with id %s not found", cls.model.__name__, model_id)
            return instance
        except SQLAlchemyError as e:
            logging.error(
                "Error fetching %s by id %s: %s",
                cls.model.__name__,
                model_id,
                e,
            )
            raise

    @classmethod
    async def update(
        cls,
        model_id: int,
        validated_values: V,
        session: AsyncSession,
    ) -> T | None:
        instance = await cls.get_by_id(model_id=model_id, session=session)
        if not instance:
            logging.warning("%s with id %s not found", cls.model.__name__, model_id)
            return None

        for field, value in validated_values.model_dump().items():
            setattr(instance, field, value)

        try:
            await session.flush()
            await session.commit()
            logging.info(
                "%s with id %s successfully updated",
                cls.model.__name__,
                model_id,
            )
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(
                "Error updating %s with id %s: %s",
                cls.model.__name__,
                model_id,
                e,
            )
            raise

        return instance

    @classmethod
    async def delete(cls, model_id: int, session: AsyncSession) -> dict:
        instance = await cls.get_by_id(model_id=model_id, session=session)
        if not instance:
            logging.warning("%s with id %s not found", cls.model.__name__, model_id)
            return {"message": f"{cls.model.__name__} not found", "deleted": False}

        try:
            await session.delete(instance)
            await session.commit()
            logging.info(
                "%s with id %s successfully deleted",
                cls.model.__name__,
                model_id,
            )
            return {
                "message": f"{cls.model.__name__} with id {model_id} deleted",
                "deleted": True,
            }
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(
                "Error deleting %s with id %s: %s",
                cls.model.__name__,
                model_id,
                e,
            )
            raise
