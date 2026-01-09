# Database Migration Guide

현재 FestAPI는 인메모리 데이터베이스를 사용하고 있습니다. 프로덕션 환경에서는 PostgreSQL, MySQL 등의 영구 데이터베이스로 마이그레이션이 필요합니다.

## 현재 상태

- **데이터베이스**: 인메모리 (Python dict)
- **위치**: `app/core/database.py`
- **제한사항**:
  - 서버 재시작 시 모든 데이터 손실
  - 수평 확장 불가 (여러 인스턴스 간 데이터 공유 불가)
  - 트랜잭션 지원 없음
  - 복잡한 쿼리 불가

## 권장 데이터베이스

### PostgreSQL (권장)
- **장점**: 안정성, 확장성, JSON 지원, 풍부한 기능
- **사용 예**: Heroku, AWS RDS, Google Cloud SQL
- **ORM**: SQLAlchemy + Alembic

### MySQL
- **장점**: 널리 사용됨, 호환성 높음
- **사용 예**: AWS RDS, PlanetScale

### MongoDB
- **장점**: 스키마리스, 빠른 개발
- **적합성**: OAuth 사용자 데이터 저장에 적합

## 마이그레이션 단계

### 1. SQLAlchemy 설치

```bash
pip install sqlalchemy alembic asyncpg psycopg2-binary
```

### 2. 데이터베이스 모델 정의

`app/models/db_models.py`:

```python
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    email = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    picture = Column(Text, nullable=True)
    verified_email = Column(Boolean, default=False)
    provider = Column(String(50), nullable=False)
    provider_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostDB(Base):
    __tablename__ = "posts"

    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TokenBlacklistDB(Base):
    __tablename__ = "token_blacklist"

    token = Column(String(500), primary_key=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)
```

### 3. 데이터베이스 연결 설정

`app/core/database.py`:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/festapi"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
```

### 4. Alembic 초기화

```bash
alembic init alembic
```

`alembic.ini` 수정:
```ini
sqlalchemy.url = postgresql+asyncpg://user:password@localhost/festapi
```

### 5. 첫 마이그레이션 생성

```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### 6. 환경 변수 추가

`.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/festapi
```

## 데이터 마이그레이션 스크립트

인메모리에서 PostgreSQL로 데이터 이전:

```python
# scripts/migrate_data.py
async def migrate_data():
    from app.core.database import db as in_memory_db
    from app.core.db_connection import async_session_maker
    from app.models.db_models import UserDB, PostDB

    async with async_session_maker() as session:
        # Migrate users
        for email, user in in_memory_db.users.items():
            db_user = UserDB(
                email=user.email,
                name=user.name,
                picture=user.picture,
                verified_email=user.verified_email,
                provider=user.provider,
                provider_id=user.provider_id
            )
            session.add(db_user)

        # Migrate posts
        for post_id, post in in_memory_db.posts.items():
            db_post = PostDB(
                id=post.id,
                title=post.title,
                content=post.content,
                author_email=post.author_email
            )
            session.add(db_post)

        await session.commit()
```

## Docker Compose 설정

`docker-compose.yml`에 PostgreSQL 추가:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: festapi
      POSTGRES_USER: festuser
      POSTGRES_PASSWORD: festpass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql+asyncpg://festuser:festpass@postgres:5432/festapi

volumes:
  postgres_data:
```

## 테스트 전략

1. **개발 환경**: SQLite (빠른 테스트)
2. **스테이징**: PostgreSQL (프로덕션과 동일)
3. **프로덕션**: PostgreSQL + 백업

## 체크리스트

- [ ] SQLAlchemy 모델 정의
- [ ] Alembic 마이그레이션 설정
- [ ] 환경별 데이터베이스 URL 설정
- [ ] 데이터베이스 연결 풀 설정
- [ ] 트랜잭션 처리 추가
- [ ] 에러 핸들링 강화
- [ ] 백업 전략 수립
- [ ] 모니터링 설정
- [ ] 성능 테스트
- [ ] 롤백 계획 수립

## 참고 자료

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [FastAPI with Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
