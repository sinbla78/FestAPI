from enum import Enum


class APIVersion(str, Enum):
    """API 버전"""
    V1 = "v1"


# 현재 API 버전
CURRENT_VERSION = APIVersion.V1

# 지원하는 API 버전 목록
SUPPORTED_VERSIONS = [APIVersion.V1]

# API 버전 정보
VERSION_INFO = {
    APIVersion.V1: {
        "version": "1.0.0",
        "status": "stable",
        "deprecated": False,
        "sunset_date": None,
        "description": "초기 안정 버전 - OAuth 2.0 인증, 게시글 CRUD, 사용자 관리"
    }
}


def get_version_info(version: APIVersion) -> dict:
    """특정 버전의 정보 반환"""
    return VERSION_INFO.get(version, {})


def is_version_supported(version: str) -> bool:
    """버전이 지원되는지 확인"""
    try:
        return APIVersion(version) in SUPPORTED_VERSIONS
    except ValueError:
        return False
