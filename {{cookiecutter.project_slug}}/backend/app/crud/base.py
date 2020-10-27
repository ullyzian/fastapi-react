from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        :param model: A SQLAlchemy model class
        """
        self.model = model

    def detail(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, *, offset: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(offset).limit(limit).all()

    def create(self, db: Session, *, data: CreateSchemaType) -> ModelType:
        attributes = jsonable_encoder(data)
        instance = self.model(**attributes)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def update(self, db: Session, *, instance: ModelType,
               data: Union[UpdateSchemaType, Dict[str, Any]]
               ) -> ModelType:
        attributes = jsonable_encoder(instance)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)
        for attr in attributes:
            if attr in update_data:
                setattr(instance, attr, update_data[attr])
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def remove(self, db: Session, *, id: int) -> ModelType:
        instance = db.query(self.model).get(id)
        db.delete(instance)
        db.commit()
        return instance
