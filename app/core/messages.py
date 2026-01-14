"""API 응답 메시지 상수 정의"""


# 공통 에러 메시지
class ErrorMessages:
    """에러 메시지 상수"""

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

    # 날짜 형식 관련
    INVALID_DATE_FORMAT = "생년월일 형식이 올바르지 않습니다. (YYYY-MM-DD)"

    # 공통 예외 메시지
    BAD_REQUEST = "잘못된 요청입니다."
    UNAUTHORIZED_FAILED = "인증에 실패했습니다."
    FORBIDDEN = "권한이 없습니다."
    RESOURCE_NOT_FOUND = "요청한 리소스를 찾을 수 없습니다."
    CONFLICT = "리소스 충돌이 발생했습니다."
    INTERNAL_SERVER_ERROR = "서버 내부 오류가 발생했습니다."
    VALIDATION_ERROR = "입력 데이터 검증에 실패했습니다."


class SuccessMessages:
    """성공 메시지 상수"""

    # 비밀번호 관련
    PASSWORD_CHANGED = "비밀번호가 성공적으로 변경되었습니다."

    # 로그아웃
    LOGOUT_SUCCESS = "성공적으로 로그아웃되었습니다."

    # 블랙리스트
    BLACKLIST_CLEANED = "만료된 블랙리스트 토큰이 정리되었습니다."
