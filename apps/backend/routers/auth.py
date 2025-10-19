from fastapi import APIRouter, Depends
from models.auth import (
    SignUpRequest, SignInRequest, AuthResponse, 
    UserProfileResponse, UpdateProfileRequest
)
from services.auth_service import (
    signup_user, signin_user, signout_user,
    get_user_profile, update_user_profile
)
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """新規ユーザー登録"""
    return await signup_user(request)

@router.post("/signin", response_model=AuthResponse)
async def signin(request: SignInRequest):
    """ユーザーログイン"""
    return await signin_user(request)

@router.post("/signout")
async def signout(current_user = Depends(get_current_user)):
    """ユーザーログアウト"""
    return await signout_user()

@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user = Depends(get_current_user)):
    """ユーザープロフィール取得"""
    return await get_user_profile(current_user.id)

@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(request: UpdateProfileRequest, current_user = Depends(get_current_user)):
    """ユーザープロフィール更新"""
    return await update_user_profile(current_user.id, current_user.email, request)