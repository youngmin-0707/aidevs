# FastAPI 게시판 CRUD

GET, POST, PUT, DELETE를 사용해 게시글을 생성·조회·수정·삭제하는 연습 프로젝트입니다.

## CRUD란?

| 글자 | 뜻 | 게시판 예시 |
| --- | --- | --- |
| C | Create (생성) | 게시글 작성 |
| R | Read (조회) | 게시글 목록 보기 |
| U | Update (수정) | 게시글 내용 수정 |
| D | Delete (삭제) | 게시글 삭제 |

## 실행 방법

```powershell
cd C:\aidevs\02_supabase-ai-backend\01_fastapi-backend\06_board
uvicorn main:app --reload
```

Swagger UI: `http://127.0.0.1:8000/docs`

## API 목록

| Method | URL | CRUD 기능 |
| --- | --- | --- |
| GET | `/posts` | Read: 전체 게시글 조회 |
| POST | `/posts` | Create: 새 게시글 생성 |
| PUT | `/posts` | Update: 기존 게시글 수정 |
| DELETE | `/posts/{post_id}` | Delete: 기존 게시글 삭제 |

게시글 날짜는 시간 없이 `YY-MM_DD` 형식으로 표시합니다. 예: `26-07_15`
