import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging():
    """로깅 설정을 초기화합니다."""

    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 로그 파일명 (날짜별)
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"

    # 로그 포맷 설정
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # 루트 로거 설정
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # 콘솔 출력
            logging.StreamHandler(sys.stdout),
            # 파일 출력
            logging.FileHandler(log_file, encoding="utf-8")
        ]
    )

    # uvicorn 로거 설정
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)

    # fastapi 로거 설정
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(logging.INFO)

    # 앱 로거 설정
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)

    return logging.getLogger("app")


# 기본 로거 인스턴스
logger = setup_logging()
