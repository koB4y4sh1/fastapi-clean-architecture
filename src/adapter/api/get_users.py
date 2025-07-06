from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from src.schema.api.user import UserResponse
from src.interface.user_interface_service import UserInterfaceService
from src.dependencies.user_dependencies import get_user_interface_service

router = APIRouter()

@router.get(
    "/users", 
    response_model=List[UserResponse],
    summary="ユーザー一覧の取得",
    description="登録されているすべてのユーザーの情報を取得します。\n\nidが指定された場合、そのユーザーの情報を返します。",
)
def get_users(
    id: Optional[int] =  Query(None, ge=0, title = "ユーザーID",description="ユーザーIDでの検索"),
    service: UserInterfaceService = Depends(get_user_interface_service) ):
    return service.get_all_users(id = id)
