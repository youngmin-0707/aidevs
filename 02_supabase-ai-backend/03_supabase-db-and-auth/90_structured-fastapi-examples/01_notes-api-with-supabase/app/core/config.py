# 학습 포인트: .env의 환경 변수와 앱 설정값을 읽고 관리하는 파일입니다.
""".env 파일을 읽어 Supabase 설정을 준비합니다."""

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
import os
# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from pathlib import Path

# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from dotenv import load_dotenv
# 학습 포인트: 아래에서 사용할 외부 모듈이나 표준 라이브러리 기능을 가져옵니다.
from supabase import create_client


# 학습 포인트: PROJECT_ROOT 변수에 오른쪽에서 만든 값을 저장합니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# 학습 포인트: 함수를 호출해 필요한 작업을 실행합니다.
load_dotenv(PROJECT_ROOT / ".env")

# 학습 포인트: SUPABASE_URL 변수에 오른쪽에서 만든 값을 저장합니다.
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
# 학습 포인트: SUPABASE_SERVICE_ROLE_KEY 변수에 오른쪽에서 만든 값을 저장합니다.
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# .env가 없는 상태에서도 /health와 테스트 앱은 시작할 수 있게 둡니다.
# 실제 /notes 요청 전에는 .env를 설정해야 합니다.
# 학습 포인트: supabase 변수에 오른쪽에서 만든 값을 저장합니다.
supabase = (
    create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
    else None
)
