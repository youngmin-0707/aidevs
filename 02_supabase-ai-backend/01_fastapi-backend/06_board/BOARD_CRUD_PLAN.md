# 게시판 CRUD 구현 계획

## 1. 목표

`01_http-methods.py`의 구성처럼 FastAPI와 GET, POST, PUT, DELETE를 사용해 간단한 게시판 API를 만든다.

CRUD는 데이터를 다루는 네 가지 기본 기능이다.

| CRUD | 뜻 | 게시판 기능 |
| --- | --- | --- |
| Create | 생성 | 새 게시글 작성 |
| Read | 조회 | 게시글 목록 보기 |
| Update | 수정 | 기존 게시글 수정 |
| Delete | 삭제 | 기존 게시글 삭제 |

## 2. 게시글 데이터

게시글 한 건은 아래 정보를 가진다.

```json
{
  "id": 1,
  "title": "첫 번째 게시글",
  "content": "FastAPI 게시판 CRUD를 연습합니다.",
  "created_date": "26-07_15",
  "updated_date": "26-07_15"
}
```

| 항목 | 역할 |
| --- | --- |
| `id` | 게시글 번호 |
| `title` | 게시글 제목 |
| `content` | 게시글 내용 |
| `created_date` | 처음 작성한 날짜 |
| `updated_date` | 마지막으로 수정한 날짜 |

날짜는 시간 없이 `YY-MM_DD` 형식으로 저장한다. 예: 2026년 7월 15일은 `26-07_15`이다.

## 3. API 구성

수업 예제의 메모 API를 게시글 API로 바꾼다.

| Method | URL | 역할 |
| --- | --- | --- |
| GET | `/posts` | 모든 게시글 조회 |
| POST | `/posts` | 새 게시글 생성 |
| PUT | `/posts` | 기존 게시글 수정 |
| DELETE | `/posts/{post_id}` | 기존 게시글 삭제 |

## 4. 코드 구성

- `PostCreate`: 게시글 작성에 필요한 `title`, `content`를 검사한다.
- `PostUpdate`: 수정할 게시글의 `id`, `title`, `content`를 검사한다.
- `posts`: 서버가 실행되는 동안 게시글을 저장하는 딕셔너리다.
- `next_post_id`: 새 게시글에 줄 다음 번호다.
- `today_date()`: 오늘 날짜를 `YY-MM_DD` 문자열로 만든다.
- 없는 게시글을 수정하거나 삭제하면 `404` 오류를 반환한다.

작성할 때 `created_date`와 `updated_date`는 같은 날짜로 저장한다. 수정할 때는 `created_date`를 유지하고 `updated_date`만 오늘 날짜로 바꾼다.

## 5. 초보자용 주석

`main.py`의 모든 학습 단위에 한국어 주석을 작성한다.

- import가 필요한 이유
- FastAPI 앱과 Pydantic 모델의 역할
- 딕셔너리 저장소와 게시글 번호의 의미
- 날짜를 만드는 방법
- 각 HTTP Method가 하는 일
- `global`, `if`, `pop`, `404` 처리의 이유

## 6. 작업 순서

1. `06_board` 폴더의 이전 구현 파일을 새 구성으로 교체한다.
2. `main.py`에 게시판 CRUD API와 모든 학습용 주석을 작성한다.
3. `README.md`에 CRUD 의미, 실행 방법, API 목록을 정리한다.
4. Swagger UI에서 GET, POST, PUT, DELETE 동작을 확인한다.
