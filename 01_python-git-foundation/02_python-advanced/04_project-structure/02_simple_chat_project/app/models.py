"""데이터 모양을 정의하는 파일입니다.

처음에는 dict만 사용해도 됩니다.
다만 dataclass를 사용하면 "이 데이터가 어떤 값을 가져야 하는지"를 더 분명하게 볼 수 있습니다.

뒤 과정의 Pydantic BaseModel도 이와 비슷하게 데이터 모양을 코드로 표현합니다.
"""

from dataclasses import asdict, dataclass


@dataclass
class ResponseChatMessage:
    """
   사용자가 입력한prompt를 전송한다.\n
   사용자 ID,방법을 같이 전송한다.
   """
    
    prompt: str
    User: str
    method: str ="온화하게"


    @dataclass
class ResponseChatMessage:
        """
   LLM을 통해 질문의 답변을 응답합니다.\n
   응답,상태메세지,모델을 전송합니다.
   """
    
    answer: str
    model: str
    msg: str ="ok"




    def to_dict(self) -> dict:
        """JSON 저장을 위해 dataclass object를 dict로 바꿉니다."""

        return asdict(self)
