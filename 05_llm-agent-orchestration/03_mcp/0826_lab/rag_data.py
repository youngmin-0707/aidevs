"""기념일 시나리오 생성에 참고할 작은 RAG 문서와 검색 함수입니다."""

from typing import Any


RAG_DOCUMENTS = [
    {
        "id": "introvert-low-surprise",
        "title": "내향형 상대를 위한 소규모 기념일 가이드",
        "tags": ["내향적", "조용한", "소규모", "서프라이즈 낮음"],
        "content": "내향적인 상대에게는 많은 사람이 보는 공개 이벤트보다 조용한 대화와 짧은 편지가 잘 어울립니다. 선택할 시간을 주고, 과한 반응을 기대하지 않습니다.",
    },
    {
        "id": "100days-guide",
        "title": "100일 기념일 구성 가이드",
        "tags": ["100일", "연인", "편지", "추억"],
        "content": "100일에는 비싼 선물 하나보다 함께 보낸 시간을 돌아보는 편지, 질문 카드, 사진 같은 작은 추억 요소를 조합할 수 있습니다.",
    },
    {
        "id": "budget-guide",
        "title": "예산 안에서 이벤트를 구성하는 방법",
        "tags": ["예산", "선물", "시간"],
        "content": "예산이 정해져 있으면 선물, 포장, 활동 비용을 나누어 계산합니다. 비용이 초과되면 선물 수를 줄이거나 편지 같은 저비용 요소를 활용합니다.",
    },
]


def retrieve_documents(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """질문과 태그가 많이 겹치는 문서를 찾아 반환합니다.

    이 함수는 벡터 DB를 연결하기 전, RAG의 검색 흐름을 쉽게 이해하기 위한
    키워드 기반 Mock 검색입니다. 나중에는 같은 입력과 출력 형태를 유지한 채
    임베딩과 pgvector 검색으로 교체할 수 있습니다.
    """
    query_lower = query.lower()
    scored = []
    for document in RAG_DOCUMENTS:
        score = sum(tag.lower() in query_lower for tag in document["tags"])
        if score:
            scored.append((score, document))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [document for _, document in scored[:top_k]]
