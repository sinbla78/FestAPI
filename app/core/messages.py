"""
API 응답 메시지 상수 정의

이 모듈은 애플리케이션 전반에 걸쳐 사용되는 에러 메시지와 성공 메시지를 중앙화하여 관리합니다.
메시지를 상수로 정의함으로써 코드 중복을 방지하고 일관성을 유지합니다.
"""


class ErrorMessages:
    """
    에러 메시지 상수

    애플리케이션에서 발생하는 모든 에러 메시지를 정의합니다.
    카테고리별로 구분되어 있어 쉽게 찾고 관리할 수 있습니다.
    """

    # 인증 관련
    INVALID_CREDENTIALS = "아이디 또는 비밀번호가 올바르지 않습니다."
    TOKEN_EXPIRED = "Token has expired"
    TOKEN_INVALID = "Invalid authentication credentials"
    TOKEN_REVOKED = "Token has been revoked"
    UNAUTHORIZED = "인증이 필요합니다."

    # 사용자 관련
    USER_NOT_FOUND = "사용자를 찾을 수 없습니다."
    USER_ALREADY_EXISTS = "이미 존재하는 아이디입니다."

    # 관리자 관련
    MANAGER_NOT_FOUND = "관리자를 찾을 수 없습니다."
    MANAGER_ALREADY_EXISTS = "이미 존재하는 아이디입니다."

    # 부서 관련
    DEPARTMENT_NOT_FOUND = "부서를 찾을 수 없습니다."
    DEPARTMENT_ALREADY_EXISTS = "이미 존재하는 부서명입니다."
    INVALID_DEPARTMENT = "존재하지 않는 부서입니다."

    # 기간제 인력 관련
    EMPLOYEE_NOT_FOUND = "기간제 인력을 찾을 수 없습니다."

    # 게시글 관련
    POST_NOT_FOUND = "게시글을 찾을 수 없습니다."
    POST_UPDATE_FORBIDDEN = "게시글을 수정할 권한이 없습니다."
    POST_DELETE_FORBIDDEN = "게시글을 삭제할 권한이 없습니다."

    # 첫 로그인 관련
    ALREADY_COMPLETED_FIRST_LOGIN = "이미 첫 로그인 정보를 입력했습니다."

    # 비밀번호 관련
    INVALID_CURRENT_PASSWORD = "현재 비밀번호가 올바르지 않습니다."
    PASSWORD_TOO_SHORT = "비밀번호는 8자 이상이어야 합니다."
    PASSWORD_TOO_LONG = "비밀번호는 30자 이하여야 합니다."
    PASSWORD_LENGTH_INVALID = "비밀번호는 8자~30자까지 작성할 수 있습니다."
    PASSWORDS_DO_NOT_MATCH = "새 비밀번호와 새 비밀번호 확인이 일치하지 않습니다."

    # 입력 검증 관련
    INVALID_DATE_FORMAT = "생년월일 형식이 올바르지 않습니다. (YYYY-MM-DD)"
    EMPTY_INPUT_NOT_ALLOWED = "공백만 입력할 수 없습니다."

    # 공통 예외 메시지
    BAD_REQUEST = "잘못된 요청입니다."
    UNAUTHORIZED_FAILED = "인증에 실패했습니다."
    FORBIDDEN = "권한이 없습니다."
    RESOURCE_NOT_FOUND = "요청한 리소스를 찾을 수 없습니다."
    CONFLICT = "리소스 충돌이 발생했습니다."
    INTERNAL_SERVER_ERROR = "서버 내부 오류가 발생했습니다."
    VALIDATION_ERROR = "입력 데이터 검증에 실패했습니다."
    RATE_LIMIT_EXCEEDED = "요청 횟수 제한을 초과했습니다. 잠시 후 다시 시도해주세요."


class SuccessMessages:
    """
    성공 메시지 상수

    작업이 성공적으로 완료되었을 때 사용되는 메시지를 정의합니다.
    """

    # 비밀번호 관련
    PASSWORD_CHANGED = "비밀번호가 성공적으로 변경되었습니다."

    # 로그아웃
    LOGOUT_SUCCESS = "성공적으로 로그아웃되었습니다."

    # 블랙리스트
    BLACKLIST_CLEANED = "만료된 블랙리스트 토큰이 정리되었습니다."
