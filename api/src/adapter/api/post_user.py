from fastapi import APIRouter, Depends
from src.interface.user_interface_service import UserInterfaceService
from src.schema.api.user import UserCreateRequest, UserResponse
from src.dependencies.user_dependencies import get_user_interface_service

router = APIRouter()

@router.post(
    "/users",
    response_model=UserResponse,
    summary="ユーザー登録",
    description="新しいユーザーを登録します。Bearerトークンが必要です。",
)
def post_user(
    user: UserCreateRequest,
    service: UserInterfaceService = Depends(get_user_interface_service)
):
    return service.create_user(user)
