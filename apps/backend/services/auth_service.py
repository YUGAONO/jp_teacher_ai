from fastapi import HTTPException
from database.supabase import SB
from models.auth import SignUpRequest, SignInRequest, AuthResponse, UserProfileResponse, UpdateProfileRequest

async def signup_user(request: SignUpRequest) -> AuthResponse:
    """新規ユーザー登録"""
    try:
        # Supabaseでユーザー作成
        auth_response = SB.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        
        if auth_response.user is None or auth_response.session is None:
            raise HTTPException(
                status_code=400,
                detail="User registration failed"
            )
        
        # プロフィール情報をprofilesテーブルに保存
        profile_data = {
            "id": auth_response.user.id,
            "display_name": request.display_name,
            "locale": request.locale,
            "current_plan": "free"
        }
        
        SB.table("profiles").insert(profile_data).execute()
        
        return AuthResponse(
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            user={
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "display_name": request.display_name,
                "locale": request.locale,
                "current_plan": "free"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

async def signin_user(request: SignInRequest) -> AuthResponse:
    """ユーザーログイン"""
    try:
        # Supabaseでログイン
        auth_response = SB.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if auth_response.user is None or auth_response.session is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )
        
        # プロフィール情報を取得
        profile_response = SB.table("profiles").select("*").eq("id", auth_response.user.id).execute()
        profile = profile_response.data[0] if profile_response.data else {}
        
        return AuthResponse(
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            user={
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "display_name": profile.get("display_name", ""),
                "locale": profile.get("locale", "ja"),
                "current_plan": profile.get("current_plan", "free")
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

async def signout_user():
    """ユーザーログアウト"""
    SB.auth.sign_out()
    return {"message": "Successfully signed out"}

async def get_user_profile(user_id: str) -> UserProfileResponse:
    """ユーザープロフィール取得"""
    profile_response = SB.table("profiles").select("*").eq("id", user_id).execute()
    
    if not profile_response.data:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )
    
    profile = profile_response.data[0]
    
    # ユーザー情報を取得（emailのため）
    user_response = SB.auth.get_user()
    email = user_response.user.email if user_response.user else ""
    
    return UserProfileResponse(
        id=profile["id"],
        email=email,
        display_name=profile["display_name"],
        locale=profile["locale"],
        current_plan=profile["current_plan"],
        created_at=profile["created_at"],
        updated_at=profile["updated_at"]
    )

async def update_user_profile(user_id: str, user_email: str, request: UpdateProfileRequest) -> UserProfileResponse:
    """ユーザープロフィール更新"""
    # 更新データを準備
    update_data = {}
    if request.display_name is not None:
        update_data["display_name"] = request.display_name
    if request.locale is not None:
        update_data["locale"] = request.locale
    if request.current_plan is not None:
        update_data["current_plan"] = request.current_plan
    
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data to update"
        )
    
    # プロフィール更新
    update_response = SB.table("profiles").update(update_data).eq("id", user_id).execute()
    
    if not update_response.data:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )
    
    profile = update_response.data[0]
    
    return UserProfileResponse(
        id=profile["id"],
        email=user_email,
        display_name=profile["display_name"],
        locale=profile["locale"],
        current_plan=profile["current_plan"],
        created_at=profile["created_at"],
        updated_at=profile["updated_at"]
    )