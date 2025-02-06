from fastapi import APIRouter
from schemas import UserBase, UserResponse, UserUpdate, UserList
from repository import UserRepository
from fastapi import Depends
from fastapi import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
async def add_user(body: UserBase):
    try:
        user_id = await UserRepository.add_user(body)
        return {"id_user": user_id}
    except Exception as e:
        return {"error": "Failed to create user"}


@router.get("", response_model=list[UserList])
async def get_users():
    users = await UserRepository.all_users()
    return users


@router.get("/{user_id}/")
async def get_user(user_id: int) -> UserResponse:
    user = await UserRepository.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}/")
async def delete_user(user_id: int):
    res = await UserRepository.delete_user(user_id)
    return res


@router.put("/{user_id}/")
async def update_user(user_id: int, user: UserUpdate = Depends()):
    res = await UserRepository.update_user(user_id, user)
    if not res:
        raise HTTPException(status_code=404, detail="User not found or not updated")
    return {"status": "success", "message": "User updated successfully"}