# 학습 포인트: .env의 환경 변수와 앱 설정값을 읽고 관리하는 파일입니다.
"""프로젝트 폴더의 .env 파일을 읽습니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from __future__ import annotations

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from pathlib import Path

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from dotenv import load_dotenv


# 학습 포인트: ENV_PATH 변수에 오른쪽에서 만든 값을 저장합니다.
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
# 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
load_dotenv(ENV_PATH)
