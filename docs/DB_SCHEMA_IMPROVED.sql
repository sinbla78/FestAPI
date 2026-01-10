-- 개선된 데이터베이스 스키마
-- 기간제 인력 관리 시스템

-- 1. 부서 테이블 (먼저 생성 - 참조되는 테이블)
CREATE TABLE departments (
    department_id BIGSERIAL PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 부서 테이블에 기본 데이터 삽입
INSERT INTO departments (department_name, description) VALUES
('인사팀', '인사 관리 담당'),
('총무팀', '총무 업무 담당'),
('재무팀', '재무 관리 담당'),
('IT팀', '정보기술 담당');

-- 2. 관리자 테이블
CREATE TABLE managers (
    manager_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 사용자 테이블 (부서 담당자)
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    department_id BIGINT NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    user_phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 4. 기간제 인력 테이블
CREATE TABLE term_employees (
    term_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    birthdate DATE NOT NULL,
    address VARCHAR(255) NOT NULL,
    hire_date DATE NOT NULL,
    termination_date DATE,
    occupation VARCHAR(255) NOT NULL,
    department_id BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'terminated', 'on_leave')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_term_employees_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_term_employees_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_dates
        CHECK (termination_date IS NULL OR termination_date >= hire_date)
);

-- 5. 인덱스 생성 (성능 최적화)
CREATE INDEX idx_users_department ON users(department_id);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_term_employees_user ON term_employees(user_id);
CREATE INDEX idx_term_employees_department ON term_employees(department_id);
CREATE INDEX idx_term_employees_status ON term_employees(status);
CREATE INDEX idx_term_employees_hire_date ON term_employees(hire_date);

-- 6. Updated_at 자동 업데이트 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 7. 트리거 생성
CREATE TRIGGER update_managers_updated_at BEFORE UPDATE ON managers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_departments_updated_at BEFORE UPDATE ON departments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_term_employees_updated_at BEFORE UPDATE ON term_employees
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 8. 뷰 생성 (조인 쿼리 간소화)
CREATE VIEW v_term_employees_detail AS
SELECT
    te.term_id,
    te.name,
    te.birthdate,
    te.address,
    te.hire_date,
    te.termination_date,
    te.occupation,
    te.status,
    d.department_name AS issuing_department,
    u.user_name AS manager_name,
    u.user_phone AS manager_phone,
    u.email AS manager_email,
    te.created_at,
    te.updated_at
FROM term_employees te
JOIN departments d ON te.department_id = d.department_id
JOIN users u ON te.user_id = u.user_id;

-- 주요 개선 사항:
-- 1. 테이블명 영문화 및 명확화
-- 2. BIGSERIAL 사용 (자동 증가 PK)
-- 3. 비밀번호는 password_hash로 명명 (해시 저장 명시)
-- 4. DATE 타입 사용 (날짜 필드)
-- 5. 외래키 제약조건 명명 및 ON DELETE/UPDATE 옵션 추가
-- 6. status 필드로 상태 관리 (active, terminated, on_leave)
-- 7. CHECK 제약조건 (퇴사일 >= 입사일)
-- 8. 인덱스 추가 (성능 최적화)
-- 9. updated_at 자동 업데이트 트리거
-- 10. 뷰 생성 (조인 쿼리 간소화)
