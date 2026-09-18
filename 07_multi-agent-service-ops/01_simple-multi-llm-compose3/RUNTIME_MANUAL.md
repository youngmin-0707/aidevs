#  실습 매뉴얼_0917 (로컬 빌드 → Docker Hub 배포 → EC2 실행)

이 문서는 `0917터미널.txt`에서 실제로 입력한 명령어를 순서대로 정리한 **실행 매뉴얼**입니다.
왜 이 실습을 하는지, Compose 파일의 구조가 무엇인지 등 수업 맥락은 아래 문서를 먼저 읽으세요.

- 기본 실행/배포 개념: `C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose\README.md`
- EC2 접속·Docker 설치·코드 전송: `C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\03_aws-ec2\03_install-and-transfer.md`
- Redis 단독 실행 개념: `C:\aidevs\05_llm-agent-orchestration\00_local-runtime\04_redis.md`
- pgvector 단독 실행 개념: `C:\aidevs\05_llm-agent-orchestration\00_local-runtime\03_postgresql-pgvector.md`
- `.env` 항목 설명: `C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose\.env.example`

## 사전 준비 체크리스트

이 값들이 없으면 아래 절차 중간에 막힙니다. 시작 전에 미리 확보하세요.

- [ ] Docker Hub 계정 (예: `young0707`) — 2번에서 이미지를 올릴 저장소
- [ ] EC2 접속용 `.pem` Key 파일 경로 — 3번, 8번에서 사용
- [ ] EC2 Public IP 또는 Public DNS — 3번, 8번에서 `<PUBLIC_IP>` 자리에 입력
- [ ] EC2 보안 그룹(Security Group) 인바운드 규칙에 `22(SSH)`, `8000(Backend)`, `8501(Frontend)` 포트가
      내 IP 또는 `0.0.0.0/0`으로 열려 있는지 확인 — 안 열려 있으면 10번의 `curl` 확인이 실패합니다.
- [ ] `OPENAI_API_KEY` 또는 `GEMINI_API_KEY` 중 최소 1개 — 없으면 Backend Health Check가 provider 오류로 막힐 수 있습니다.

## 목차

- [실습 매뉴얼\_0917 (로컬 빌드 → Docker Hub 배포 → EC2 실행)](#실습-매뉴얼_0917-로컬-빌드--docker-hub-배포--ec2-실행)
  - [사전 준비 체크리스트](#사전-준비-체크리스트)
  - [목차](#목차)
  - [1. 로컬: Docker Compose로 이미지 빌드](#1-로컬-docker-compose로-이미지-빌드)
  - [2. 로컬: Docker Hub 로그인 및 이미지 태그·푸시](#2-로컬-docker-hub-로그인-및-이미지-태그푸시)
  - [3. 로컬: EC2 서버 접속](#3-로컬-ec2-서버-접속)
  - [4. EC2: 패키지 최신화 및 Docker 확인](#4-ec2-패키지-최신화-및-docker-확인)
  - [5. EC2: Redis 단독 컨테이너 실행](#5-ec2-redis-단독-컨테이너-실행)
  - [6. EC2: pgvector(PostgreSQL) 단독 컨테이너 실행](#6-ec2-pgvectorpostgresql-단독-컨테이너-실행)
  - [7. EC2: DB 스키마 초기화 (psql)](#7-ec2-db-스키마-초기화-psql)
  - [8. 로컬 → EC2: 배포 파일 전송 (scp)](#8-로컬--ec2-배포-파일-전송-scp)
  - [9. EC2: 전송 파일 권한 설정](#9-ec2-전송-파일-권한-설정)
  - [10. EC2: compose.release.yml로 최종 배포 및 헬스체크](#10-ec2-composereleaseyml로-최종-배포-및-헬스체크)

---

## 1. 로컬: Docker Compose로 이미지 빌드

준비물: `compose.yml`, `backend/`, `frontend/` 폴더가 현재 위치에 있어야 합니다. (`README.md` 1번 항목 참고)

```powershell
# compose.yml에 정의된 backend, frontend 서비스의 Docker Image를 빌드
docker compose build
```

결과: `simple-app-backend:latest`, `simple-app-frontend:latest` 두 이미지가 로컬에 생성됩니다.

## 2. 로컬: Docker Hub 로그인 및 이미지 태그·푸시

준비물: Docker Hub 계정(예: `young0707`)으로 미리 로그인 가능한 상태여야 합니다.

```powershell
# 로컬 이미지 목록 확인 (오타 dopcker 주의 → docker)
docker image ls

# Docker Hub 계정으로 로그인 (저장된 인증정보 있으면 자동 재인증)
docker login

# 로컬 이미지에 "Docker Hub 계정명/저장소명:버전" 형식으로 태그 부여
docker tag simple-app-backend:latest young0707/simple-app-backend:1.0.0
docker tag simple-app-frontend:latest young0707/simple-app-frontend:1.0.0

# 태그 지정된 이미지를 Docker Hub로 업로드
docker push young0707/simple-app-backend:1.0.0
docker push young0707/simple-app-frontend:1.0.0
```

## 3. 로컬: EC2 서버 접속

준비물: 발급받은 `.pem` Key 파일 경로가 정확해야 합니다. (`03_install-and-transfer.md` 1번 항목 참고)

```powershell
# -i: SSH 접속에 사용할 Private Key 파일 지정
# ubuntu@<Public IP>: EC2 사용자 계정과 접속 주소
ssh -i agentkey.pem ubuntu@16.184.2.191
```

> `.pem` 파일이 현재 폴더에 없으면 `Permission denied (publickey)` 오류가 발생합니다.
> Key 파일이 있는 폴더로 이동한 뒤 다시 실행해야 합니다.

## 4. EC2: 패키지 최신화 및 Docker 확인

```bash
# 패키지 목록 최신화 (Ubuntu는 yum이 아니라 apt 사용)
sudo apt update

# Docker 엔진, Compose 플러그인, git, curl 설치(이미 설치돼 있으면 최신 버전 확인만)
sudo apt install -y docker.io docker-compose-v2 git curl

# Docker 서비스를 지금 시작하고, 서버 재부팅 시에도 자동 시작되도록 설정
sudo systemctl enable --now docker

# Docker 명령 줄 도구 버전 확인
docker version

# Docker Compose 플러그인 버전 확인
docker compose version
```

## 5. EC2: Redis 단독 컨테이너 실행

개념 설명: `C:\aidevs\05_llm-agent-orchestration\00_local-runtime\04_redis.md`

```bash
# -d: 백그라운드 실행 / --restart unless-stopped: 서버 재부팅 시 자동 재시작
# -p 6379:6379: 호스트 6379 포트를 컨테이너 6379 포트에 연결
# -v aidevs-redis-data:/data: 데이터 유지를 위한 named volume 마운트
# redis-server --appendonly yes: AOF(Append Only File) 영속성 옵션 활성화
sudo docker run -d --name aidevs-redis --restart unless-stopped \
  -p 6379:6379 -v aidevs-redis-data:/data \
  redis:7 redis-server --appendonly yes

# 컨테이너 안에서 redis-cli로 정상 응답(PONG) 확인
docker exec -it aidevs-redis redis-cli PING
```

## 6. EC2: pgvector(PostgreSQL) 단독 컨테이너 실행

개념 설명: `C:\aidevs\05_llm-agent-orchestration\00_local-runtime\03_postgresql-pgvector.md`

```bash
# -e: 컨테이너 최초 생성 시 DB/계정/비밀번호를 환경변수로 지정
# -v aidevs-pgvector-data:/var/lib/postgresql/data: DB 데이터 영속 저장
sudo docker run -d --name aidevs-pgvector --restart unless-stopped \
  -p 5432:5432 \
  -e POSTGRES_DB=agent_db \
  -e POSTGRES_USER=agent_user \
  -e POSTGRES_PASSWORD=agent_password \
  -v aidevs-pgvector-data:/var/lib/postgresql/data \
  pgvector/pgvector:pg16

# DB가 접속 요청을 받을 준비가 됐는지 확인
sudo docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
```

## 7. EC2: DB 스키마 초기화 (psql)

준비물: 6번에서 pgvector 컨테이너가 정상 기동 중이어야 합니다.

```bash
# 컨테이너 안의 psql로 접속 (agent_user 계정, agent_db 데이터베이스)
docker exec -it aidevs-pgvector psql -U agent_user -d agent_db
```

접속 후 psql 프롬프트(`agent_db=#`)에서 실행:

```sql
-- 이 프로젝트 전용 스키마 생성 (이미 있으면 건너뜀)
CREATE SCHEMA IF NOT EXISTS simple_multi_llm;

-- 사용자가 남긴 여행 메모 저장 테이블
CREATE TABLE IF NOT EXISTS simple_multi_llm.notes (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    message VARCHAR(500) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 채팅 대화 이력 저장 테이블 (역할은 user/assistant만 허용)
CREATE TABLE IF NOT EXISTS simple_multi_llm.chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- session_id 기준 조회 속도를 높이기 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_chat_messages_session
ON simple_multi_llm.chat_messages (session_id, id);

-- 테이블이 정상 생성됐는지 조회로 확인
SELECT * FROM simple_multi_llm.notes;

-- psql 종료
\q
```

## 8. 로컬 → EC2: 배포 파일 전송 (scp)

준비물: EC2에 업로드할 `.env`, `compose.release.yml` 파일이 로컬에 준비돼 있어야 합니다.
`.env`는 API Key 등 비밀 정보가 들어있으므로 필요한 파일만 골라서 전송합니다.
(`03_install-and-transfer.md` 5번 항목 참고)

```bash
# EC2에 업로드 대상 폴더 생성
mkdir test && cd test
```

```powershell
# 로컬 PowerShell에서 실행: 지정한 EC2 경로로 파일 복사
scp -i agentkey.pem .env ubuntu@16.184.2.191:/home/ubuntu/test
scp -i agentkey.pem compose.release.yml ubuntu@16.184.2.191:/home/ubuntu/test
```

## 9. EC2: 전송 파일 권한 설정

`.env`에 비밀 정보(API Key 등)가 있으므로 소유자만 읽고 쓸 수 있게 제한합니다.

```bash
# .env: 소유자만 읽기/쓰기 가능 (rw-------)
chmod 600 .env

# compose.release.yml: 소유자 읽기/쓰기, 그 외는 읽기만 가능 (rw-r--r--)
chmod 644 compose.release.yml
```

## 10. EC2: compose.release.yml로 최종 배포 및 헬스체크

준비물: `.env`에 `BACKEND_IMAGE`, `FRONTEND_IMAGE` 등이 2번에서 푸시한 이미지 주소로 설정돼 있어야 합니다.

```bash
# compose.release.yml에 정의된 이미지를 Docker Hub에서 받아와 컨테이너 실행
sudo docker compose -f compose.release.yml up -d
sudo docker compose -f compose.release.yml ps

# backend가 헬스체크 실패로 unhealthy면, .env 값을 nano로 수정한 뒤
# backend 서비스만 강제로 다시 만들어 재기동
nano .env
sudo docker compose -f compose.release.yml up -d --force-recreate --no-deps backend

# 컨테이너 상태 및 백엔드 헬스체크 엔드포인트 응답 확인
sudo docker compose -f compose.release.yml ps
curl -s http://127.0.0.1:8000/health
```

정상이라면 `{"status":"ok", ...}` 형태의 응답과 함께 `redis`, `database`, `providers` 항목이
모두 `true`로 표시됩니다.
