from sqlalchemy import select, delete, update
from dp import async_session
from schemas import UserResponse, UserUpdate, UserList
from models import User


class UserRepository:
    @classmethod
    async def add_user(cls, user_data: UserUpdate) -> int:
        async with async_session() as session:
            user_data = user_data.model_dump()

            user = User(**user_data)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id_user

    @classmethod
    async def get_user(cls, user_id: int):
        async with async_session() as session:
            query = select(User).where(User.id_user == user_id)
            result = await session.execute(query)
            user_model = result.scalar_one_or_none()

            if user_model:
                return UserResponse.model_validate(user_model.__dict__)

            return None

    @classmethod
    async def delete_user(cls, user_id) -> bool:
        async with async_session() as session:
            query = delete(User).where(User.id_user == user_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def update_user(cls, user_id: int, user_data: UserUpdate) -> bool:
        async with async_session() as session:
            user_data = user_data.model_dump()
            query = (
                update(User)
                .where(User.id_user == user_id)
                .values(**user_data)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def all_users(cls) -> list[UserList]:
        async with async_session() as session:
            query = select(User)
            result = await session.execute(query)
            user_models = result.scalars().all()

            user_schemas = [
                UserList.model_validate(user.__dict__) for user in user_models
            ]
            return user_schemas
