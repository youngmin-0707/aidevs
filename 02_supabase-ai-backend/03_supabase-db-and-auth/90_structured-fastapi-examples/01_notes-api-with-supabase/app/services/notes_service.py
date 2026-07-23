# 학습 포인트: 데이터베이스·AI·캐시를 사용해 실제 업무를 처리하는 서비스 파일입니다.
"""Supabase의 ex90_notes 테이블을 읽고 쓰는 코드입니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.config import supabase
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.note_schema import NoteCreate, NotePublic, NoteUpdate


# 학습 포인트: TABLE_NAME 변수에 오른쪽에서 만든 값을 저장합니다.
TABLE_NAME = "ex90_notes"


# 학습 포인트: list_notes 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def list_notes() -> list[NotePublic]:
    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return [NotePublic.model_validate(row) for row in result.data]


# 학습 포인트: create_note 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def create_note(note: NoteCreate) -> NotePublic:
    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = (
        supabase
        .table(TABLE_NAME)
        .insert({"title": note.title, "content": note.content})
        .execute()
    )
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return NotePublic.model_validate(result.data[0])


# 학습 포인트: get_note 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def get_note(note_id: str) -> NotePublic | None:
    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .eq("id", note_id)
        .limit(1)
        .execute()
    )
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not result.data:
        # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
        return None
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return NotePublic.model_validate(result.data[0])


# 학습 포인트: update_note 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def update_note(note_id: str, note: NoteUpdate) -> NotePublic | None:
    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = (
        supabase
        .table(TABLE_NAME)
        .update({"title": note.title, "content": note.content})
        .eq("id", note_id)
        .execute()
    )
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not result.data:
        # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
        return None
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return NotePublic.model_validate(result.data[0])


# 학습 포인트: delete_note 함수를 정의합니다. 입력값을 받아 정해진 작업을 처리합니다.
def delete_note(note_id: str) -> bool:
    # 학습 포인트: result 변수에 처리하거나 조회한 결과를 저장합니다.
    result = (
        supabase
        .table(TABLE_NAME)
        .delete()
        .eq("id", note_id)
        .execute()
    )
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return bool(result.data)
