-- 01_notes-api-with-supabase 예제에서 사용하는 테이블입니다.
--
-- 이 예제의 목표:
-- 1. FastAPI 구조를 router/schema/service로 나눕니다.
-- 2. service 계층에서 Supabase 테이블을 CRUD합니다.
-- 3. 인증/RLS 없이 가장 단순한 DB 연결 흐름부터 확인합니다.

create table if not exists ex90_notes (
  -- id는 각 노트를 구분하는 고유값입니다.
  -- gen_random_uuid()는 Supabase/PostgreSQL이 자동으로 uuid를 만들어 줍니다.
  id uuid primary key default gen_random_uuid(),

  -- title/content는 사용자가 입력하는 필수 텍스트입니다.
  title text not null,
  content text not null,

  -- created_at은 row가 만들어진 시간을 자동 기록합니다.
  created_at timestamp not null default now()
);


INSERT INTO ex90_notes (title, content)
VALUES
  ('FastAPI 시작하기', 'FastAPI 프로젝트의 기본 구조와 실행 방법을 정리한 노트입니다.'),
  ('Supabase 연결 설정', '환경 변수를 사용하여 Supabase 클라이언트를 설정하는 방법입니다.'),
  ('노트 생성 API', '새로운 노트를 데이터베이스에 저장하는 POST API 구현 내용입니다.'),
  ('노트 목록 조회', '저장된 모든 노트를 조회하는 GET API 구현 내용입니다.'),
  ('노트 상세 조회', 'UUID를 이용하여 특정 노트를 조회하는 방법을 정리했습니다.'),
  ('노트 수정 API', '기존 노트의 제목과 내용을 수정하는 PUT API 구현 내용입니다.'),
  ('노트 삭제 API', '선택한 노트를 삭제하는 DELETE API 구현 내용입니다.'),
  ('예외 처리 방법', '데이터가 없거나 요청이 잘못된 경우의 예외 처리 방법입니다.'),
  ('Pydantic 스키마', '요청 및 응답 데이터 검증을 위한 Pydantic 모델 설명입니다.'),
  ('API 테스트 결과', 'Swagger UI를 이용한 노트 CRUD API 테스트 결과입니다.');
  