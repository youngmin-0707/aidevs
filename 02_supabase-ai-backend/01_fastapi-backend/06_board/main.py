"""GET, POST, PUT, DELETE로 만드는 간단한 게시판 CRUD API."""

# date는 시간 없이 오늘 날짜만 가져올 때 사용합니다.
from datetime import date

# FastAPI는 API를 만들고, HTTPException은 오류 응답을 만들 때 사용합니다.
from fastapi import FastAPI, HTTPException

# BaseModel은 입력 데이터의 형식을 만들고, Field는 입력값을 검사합니다.
from pydantic import BaseModel, Field


# FastAPI 앱을 만듭니다.
# uvicorn main:app --reload 명령에서 app은 이 변수 이름을 의미합니다.
app = FastAPI(title="Board CRUD Practice")


class PostCreate(BaseModel):
    """POST 요청으로 새 게시글을 만들 때 받는 데이터입니다."""

    # 제목은 한 글자 이상 입력해야 합니다.
    title: str = Field(min_length=1, examples=["FastAPI 게시판 과제"])
    # 내용도 한 글자 이상 입력해야 합니다.
    content: str = Field(min_length=1, examples=["CRUD를 연습합니다."])


class PostUpdate(BaseModel):
    """PUT 요청으로 기존 게시글을 수정할 때 받는 데이터입니다."""

    # 수정할 게시글 번호입니다. 1 이상의 숫자만 허용합니다.
    id: int = Field(ge=1, examples=[1])
    # 수정할 제목입니다.
    title: str = Field(min_length=1, examples=["수정한 제목"])
    # 수정할 내용입니다.
    content: str = Field(min_length=1, examples=["수정한 내용입니다."])


# 게시글을 임시로 저장할 딕셔너리입니다.
# 서버를 다시 실행하면 이 데이터는 처음 상태로 돌아갑니다.
# 딕셔너리의 키는 게시글 번호, 값은 게시글 정보입니다.
posts = {
    1: {
        "id": 1,
        "title": "첫 번째 게시글",
        "content": "FastAPI 게시판 CRUD를 연습합니다.",
        "created_date": "26-07_15",
        "updated_date": "26-07_15",
    }
}

# 새 게시글에 줄 다음 번호입니다.
next_post_id = 2


def today_date() -> str:
    """오늘 날짜를 YY-MM_DD 형식의 문자열로 반환합니다."""

    # 예: 2026년 7월 15일은 "26-07_15"가 됩니다.
    return date.today().strftime("%y-%m_%d")


@app.get("/posts")
def list_posts():
    """Read: 저장된 모든 게시글을 조회합니다."""

    # values()로 게시글 정보만 꺼내고, list로 바꿔 응답합니다.
    return {"data": list(posts.values())}


@app.post("/posts", status_code=201)
def create_post(post: PostCreate):
    """Create: 새 게시글을 생성합니다."""

    # 함수 밖의 next_post_id 값을 수정하기 위해 global을 선언합니다.
    global next_post_id

    # 새 게시글을 처음 만들 때 작성일과 수정일은 같습니다.
    current_date = today_date()
    new_post = {
        "id": next_post_id,
        "title": post.title,
        "content": post.content,
        "created_date": current_date,
        "updated_date": current_date,
    }

    # 새 게시글을 저장하고 다음 게시글 번호를 하나 증가시킵니다.
    posts[next_post_id] = new_post
    next_post_id += 1

    return {"message": "post created", "data": new_post}


@app.put("/posts")
def update_post(post: PostUpdate):
    """Update: 기존 게시글의 제목과 내용을 수정합니다."""

    # 수정하려는 게시글 번호가 없으면 404 오류를 반환합니다.
    if post.id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    # 작성 날짜는 유지하고 수정 날짜만 오늘 날짜로 바꿉니다.
    posts[post.id] = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_date": posts[post.id]["created_date"],
        "updated_date": today_date(),
    }

    return {"message": "post updated", "data": posts[post.id]}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    """Delete: 게시글 한 건을 삭제합니다."""

    # 삭제하려는 게시글 번호가 없으면 404 오류를 반환합니다.
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    # pop은 게시글을 꺼내면서 딕셔너리에서 동시에 삭제합니다.
    deleted_post = posts.pop(post_id)
    return {"message": "post deleted", "data": deleted_post}
