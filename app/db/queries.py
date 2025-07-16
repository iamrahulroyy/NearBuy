# from sqlmodel import SQLModel, Session, select
# from typing import Type, TypeVar, Optional, List, Any
# from fastapi import HTTPException

# T = TypeVar("T", bound=SQLModel)


# def insert_instance(session: Session, model: Type[T], data: dict) -> T:
#     instance = model.model_validate(data)
#     session.add(instance)
#     session.commit()
#     session.refresh(instance)
#     return instance


# def update_instance(session: Session, model: Type[T], instance_id: Any, data: dict) -> T:
#     instance = session.get(model, instance_id)
#     if not instance:
#         raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
#     instance.sqlmodel_update(data)
#     session.add(instance)
#     session.commit()
#     session.refresh(instance)
#     return instance


# def delete_instance(session: Session, model: Type[T], instance_id: Any) -> None:
#     instance = session.get(model, instance_id)
#     if not instance:
#         raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
#     session.delete(instance)
#     session.commit()


# def get_instance(session: Session, model: Type[T], instance_id: Any) -> T:
#     instance = session.get(model, instance_id)
#     if not instance:
#         raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
#     return instance


# def get_all_instances(session: Session, model: Type[T]) -> List[T]:
#     return session.exec(select(model)).all()

# def paginate_instances(
#     session: Session,
#     model: Type[T],
#     page: int = 1,
#     page_size: int = 10
# ) -> List[T]:
#     if page < 1 or page_size < 1:
#         raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    
#     offset = (page - 1) * page_size
#     statement = select(model).offset(offset).limit(page_size)
#     return session.exec(statement).all()