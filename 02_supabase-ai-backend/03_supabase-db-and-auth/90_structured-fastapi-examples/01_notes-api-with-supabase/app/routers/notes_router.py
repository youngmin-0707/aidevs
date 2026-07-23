# 학습 포인트: HTTP 요청을 받아 서비스 함수로 전달하고 응답을 만드는 라우터 파일입니다.
"""URL과 HTTP 요청/응답만 담당하는 Notes API 라우터입니다."""

# 학습 포인트: FastAPI 앱과 요청 처리에 필요한 기능을 가져옵니다.
from fastapi import APIRouter, HTTPException, status

# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.core.config import SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.schemas.note_schema import NoteCreate, NotePublic, NoteUpdate
# 학습 포인트: 현재 프로젝트의 다른 계층에 정의된 기능을 가져와 연결합니다.
from app.services import notes_service


# 학습 포인트: 관련 API 주소를 묶어 관리할 라우터 객체를 만듭니다.
router = APIRouter(tags=["notes"])


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/health")
def health() -> dict[str, str | bool]:
    """서버와 Supabase 설정 상태를 확인합니다."""
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {
        "status": "ok",
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY),
    }


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/notes")
def list_notes() -> dict[str, int | list[NotePublic]]:
    # 학습 포인트: notes 변수에 오른쪽에서 만든 값을 저장합니다.
    notes = notes_service.list_notes()
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {"count": len(notes), "data": notes}


# 학습 포인트: POST 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.post("/notes", response_model=NotePublic, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> NotePublic:
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return notes_service.create_note(note)


# 학습 포인트: GET 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.get("/notes/{note_id}", response_model=NotePublic)
def get_note(note_id: str) -> NotePublic:
    # 학습 포인트: note 변수에 오른쪽에서 만든 값을 저장합니다.
    note = notes_service.get_note(note_id)
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if note is None:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=404, detail="Note not found")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return note


# 학습 포인트: 수정 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.put("/notes/{note_id}", response_model=NotePublic)
def update_note(note_id: str, note: NoteUpdate) -> NotePublic:
    # 학습 포인트: updated_note 변수에 오른쪽에서 만든 값을 저장합니다.
    updated_note = notes_service.update_note(note_id, note)
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if updated_note is None:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=404, detail="Note not found")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return updated_note


# 학습 포인트: DELETE 요청이 오면 아래 함수를 실행하도록 API 주소를 등록합니다.
@router.delete("/notes/{note_id}")
def delete_note(note_id: str) -> dict[str, str]:
    # 학습 포인트: deleted 변수에 오른쪽에서 만든 값을 저장합니다.
    deleted = notes_service.delete_note(note_id)
    # 학습 포인트: 조건이 참일 때만 들여쓰기된 코드를 실행합니다.
    if not deleted:
        # 학습 포인트: 현재 처리를 중단하고 호출한 쪽에 오류를 전달합니다.
        raise HTTPException(status_code=404, detail="Note not found")
    # 학습 포인트: 함수를 끝내고 처리 결과를 호출한 곳으로 돌려줍니다.
    return {"message": "deleted"}
