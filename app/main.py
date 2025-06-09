from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import settings
from app.routers import auth, users, protected
from app.database import db

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Google과 Apple OAuth를 지원하는 인증 시스템"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(protected.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    """OAuth 로그인 테스트 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi OAuth 로그인</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            .login-button { 
                display: inline-block; 
                padding: 12px 24px; 
                margin: 10px; 
                text-decoration: none; 
                border-radius: 6px; 
                font-weight: bold;
                text-align: center;
                min-width: 200px;
            }
            .google { background-color: #4285f4; color: white; }
            .apple { background-color: #000; color: white; }
            .endpoints { background-color: #f5f5f5; padding: 15px; border-radius: 6px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>🔐 Multi OAuth 인증 서비스</h1>
        <p>Google 또는 Apple 계정으로 로그인하세요:</p>
        
        <div>
            <a href="/auth/google" class="login-button google">🔵 Google로 로그인</a>
            <a href="/auth/apple" class="login-button apple">🍎 Apple로 로그인</a>
        </div>
        
        <div class="endpoints">
            <h3>📋 사용 가능한 엔드포인트:</h3>
            <ul>
                <li><code>GET /auth/google</code> - Google 로그인</li>
                <li><code>GET /auth/apple</code> - Apple 로그인</li>
                <li><code>GET /auth/me</code> - 내 프로필 (토큰 필요)</li>
                <li><code>GET /users</code> - 사용자 목록 (토큰 필요)</li>
                <li><code>GET /protected</code> - 보호된 페이지 (토큰 필요)</li>
                <li><code>GET /docs</code> - API 문서</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "active_users": len(db.users),
        "active_sessions": db.get_active_sessions_count(),
        "supported_providers": ["google", "apple"]
    }