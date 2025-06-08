from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

# FastAPI 앱 인스턴스 생성
app = FastAPI(title="간단한 FastAPI 서버", version="1.0.0")

# 데이터 모델 정의
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class User(BaseModel):
    username: str
    email: str
    age: Optional[int] = None

# 메모리에 저장할 간단한 데이터
items_db = []
users_db = []

# 기본 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "안녕하세요! FastAPI 서버입니다."}

# 상품 관련 엔드포인트
@app.get("/items")
async def get_items():
    return {"items": items_db}

@app.post("/items")
async def create_item(item: Item):
    items_db.append(item.dict())
    return {"message": "상품이 추가되었습니다.", "item": item}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < len(items_db):
        return {"item": items_db[item_id]}
    return {"error": "상품을 찾을 수 없습니다."}

# 사용자 관련 엔드포인트
@app.get("/users")
async def get_users():
    return {"users": users_db}

@app.post("/users")
async def create_user(user: User):
    users_db.append(user.dict())
    return {"message": "사용자가 등록되었습니다.", "user": user}

# 쿼리 파라미터 예제
@app.get("/search")
async def search_items(q: Optional[str] = None, limit: int = 10):
    if q:
        # 간단한 검색 (이름에 검색어가 포함된 상품)
        results = [item for item in items_db if q.lower() in item.get("name", "").lower()]
        return {"query": q, "results": results[:limit]}
    return {"message": "검색어를 입력해주세요.", "all_items": items_db[:limit]}

# 헬스 체크
@app.get("/health")
async def health_check():
    return {"status": "healthy", "server": "running"}

# 서버 실행을 위한 메인 함수
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)