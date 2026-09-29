# Docker Compose + GitHub Actions CI/CD 배포 — 따라하기 실습 가이드

- 수업일: 2026-09-21
- 기반 자료: 수업 요약 2건(Docker Compose CI/CD 배포), 실습 README 2건(05 Stateless / 06 Stateful)
- 이 문서의 목적: 위에서부터 순서대로 코드 블록을 복사해 붙여넣으면 오늘 실습을 그대로 재현할 수 있게 정리한 문서입니다.

---

<a id="toc"></a>

## 목차

각 제목 아래의 `↑ 목차로 이동` 링크를 누르면 이 목차로 돌아옵니다.

- [0. 이 문서 사용법](#s0)
  - [0-1. 표기 규칙](#s0-1)
  - [0-2. 오늘 실습 순서 한눈에 보기](#s0-2)
- [1. 큰 그림 (먼저 읽기)](#s1)
  - [1-1. 전체 흐름](#s1-1)
  - [1-2. 비유로 이해하기](#s1-2)
  - [1-3. 오늘 배우는 세 프로젝트의 차이](#s1-3)
- [2. 반드시 지킬 핵심 규칙 6가지](#s2)
- [Part A. 한 번만 하는 준비](#part-a)
  - [A-1. \[내 PC\] 도구 확인](#a-1)
  - [A-2. \[GitHub 웹\] 저장소와 Workflow 파일 위치 확인](#a-2)
  - [A-3. \[AWS 웹\] EC2 서버 만들기 (05에서 이미 만들었다면 건너뛰기)](#a-3)
  - [A-4. \[내 PC → EC2\] SSH 접속과 Docker 설치](#a-4)
  - [A-5. \[GitHub 웹\] production Environment 와 Secret 4개 등록](#a-5)
  - [A-6. 주의: GitHub Runner 가 EC2 의 SSH(22)에 들어올 수 있어야 CD 가 됩니다](#a-6)
- [Part B. 실습 1 — 05 Weather MCP (Stateless, Compose 1개)](#part-b)
  - [B-1. \[내 PC\] 환경 파일 만들기](#b-1)
  - [B-2. \[내 PC\] 로컬에서 실행해 보기](#b-2)
  - [B-3. \[내 PC\] 로컬에서 CI 명령 미리 실행 (= 로컬 CI)](#b-3)
  - [B-4. \[내 PC → GitHub\] 개인 브랜치에 push 해서 CI 확인](#b-4)
  - [B-5. \[내 PC → EC2\] 서버에 환경 파일(.env) 넣기](#b-5)
  - [B-6. \[GitHub 웹\] main 병합 → 승인 → 자동 배포 (CD)](#b-6)
  - [B-7. 배포 결과 확인](#b-7)
- [Part C. 실습 2 — Mini Agent 01 LLM 프로젝트를 CI/CD 로 배포 (수업 시연)](#part-c)
  - [C-1. \[내 PC\] 프로젝트에 있어야 하는 파일 확인](#c-1)
  - [C-2. \[내 PC\] 개발용 .env 와 Compose용 환경 파일 분리](#c-2)
  - [C-3. \[내 PC\] 백엔드 테스트 프로그램 준비](#c-3)
  - [C-4. \[내 PC\] 로컬 테스트 실행](#c-4)
  - [C-5. \[내 PC\] 로컬 CI: Compose 검사와 이미지 빌드](#c-5)
  - [C-6. \[내 PC\] Workflow 파일 확인 (수정할 곳 3군데)](#c-6)
  - [C-7. \[GitHub 웹\] Environment / Secret 확인](#c-7)
  - [C-8. \[EC2\] 서버에 배포 폴더와 환경 파일 미리 만들기 (오류 예방)](#c-8)
  - [C-9. \[내 PC → GitHub\] main 에 push 해서 CI/CD 실행](#c-9)
- [Part D. 실습 3 — 06 Stateful Weather (인프라와 애플리케이션 분리)](#part-d)
  - [D-1. \[내 PC\] 06 환경 파일 만들기](#d-1)
  - [D-2. \[내 PC\] 1단계 — 인프라(PostgreSQL, Redis) 먼저 실행](#d-2)
  - [D-3. \[내 PC\] 2단계 — 애플리케이션 실행](#d-3)
  - [D-4. \[내 PC\] 로컬 CI 실행](#d-4)
  - [D-5. \[GitHub 웹\] 05 Workflow 비활성화, 06 Workflow 활성화](#d-5)
  - [D-6. \[내 PC → GitHub\] 개인 브랜치에서 CI 확인](#d-6)
  - [D-7. \[EC2\] 05 → 06 서버 전환 (같은 EC2 재사용)](#d-7)
  - [D-8. \[내 PC → EC2\] 06 전용 환경 파일 서버에 전송](#d-8)
  - [D-9. \[GitHub 웹\] 최초 자동 배포 (인프라 + 애플리케이션)](#d-9)
- [Part E. 오후 팀 과제 — 초기화 후 스스로 구성해 보기](#part-e)
  - [E-1. 기존 실습 환경 정리](#e-1)
  - [E-2. 프로젝트 선택](#e-2)
  - [E-3. 팀 역할 분담 (4명 기준)](#e-3)
- [Part F. 최종 체크리스트](#part-f)
  - [로컬 준비](#f-1)
  - [로컬 CI](#f-2)
  - [GitHub](#f-3)
  - [AWS 서버](#f-4)
  - [배포 결과](#f-5)

---

<a id="s0"></a>

## 0. 이 문서 사용법

[↑ 목차로 이동](#toc)

<a id="s0-1"></a>

### 0-1. 표기 규칙

[↑ 목차로 이동](#toc)

| 표기 | 의미 |
| --- | --- |
| `[내 PC]` | 내 컴퓨터 터미널 (Windows PowerShell) |
| `[EC2]` | AWS 서버에 SSH로 접속한 터미널 (Linux bash) |
| `[GitHub 웹]` | 브라우저에서 GitHub 화면 클릭 |
| `<대괄호>` | 내 값으로 바꿔야 하는 자리. 예: `<PUBLIC_IPV4_OR_DNS>` → `3.35.10.20` |
| `#` 로 시작하는 줄 | 한글 주석. 복사해도 실행에 영향 없음 |

<a id="s0-2"></a>

### 0-2. 오늘 실습 순서 한눈에 보기

[↑ 목차로 이동](#toc)

| 순서 | 내용 | 한 번만? |
| --- | --- | --- |
| 1장 | 큰 그림과 핵심 규칙 | - |
| Part A | 도구 확인 · EC2 서버 · GitHub 설정 | 한 번만 (이후 프로젝트에서 재사용) |
| Part B | 실습 1: 05 Weather MCP (Compose 1개) | 프로젝트마다 |
| Part C | 실습 2: Mini Agent 01 LLM (수업 시연 프로젝트) | 프로젝트마다 |
| Part D | 실습 3: 06 Stateful (인프라 + 애플리케이션 분리) | 프로젝트마다 |
| Part E | 오후 팀 과제 (초기화 후 직접 구성) | - |
| Part F | 최종 체크리스트 | 마무리 |

---

<a id="s1"></a>

## 1. 큰 그림 (먼저 읽기)

[↑ 목차로 이동](#toc)

<a id="s1-1"></a>

### 1-1. 전체 흐름

[↑ 목차로 이동](#toc)

```text
내 PC에서 코드 작성
  → 로컬에서 테스트 + Compose 검사 + 이미지 빌드   (= 로컬 CI, 실패하면 여기서 고침)
  → GitHub에 push
  → GitHub Actions가 CI 자동 실행                  (테스트 · Compose 검사 · 이미지 빌드)
  → CI 통과하면 CD 실행                            (SSH로 AWS EC2 접속 → docker compose up)
  → 브라우저로 http://<EC2 IP>:8501 접속해서 확인
```

<a id="s1-2"></a>

### 1-2. 비유로 이해하기

[↑ 목차로 이동](#toc)

| 용어 | 비유 |
| --- | --- |
| CI (지속적 통합) | 공장에서 제품을 출고하기 전에 하는 **품질검사** (테스트, 설정 검사, 조립 시험) |
| CD (지속적 배포) | 검사를 통과한 제품을 **매장(서버)에 실제로 배송·진열**하는 일 |
| `compose.yml` | 여러 컨테이너를 한 번에 세우는 **조립 설명서** |
| `.env` / 환경 파일 | 서버마다 다른 값(주소, 포트, API 키)을 적어 두는 **개인 메모지**. 설명서(코드)는 그대로 두고 메모지만 바꿔 끼운다 |
| 컨테이너 안의 `127.0.0.1` | 자기 자신을 가리키는 **"나"** 라는 말. 다른 컨테이너를 부르려면 `backend` 처럼 **서비스 이름(이름표)** 으로 불러야 한다 |
| 인프라 먼저, 앱 나중 | 식당에서 **주방(DB·Redis)** 을 먼저 열어야 **홀 직원(백엔드)** 이 일할 수 있는 것과 같다 |

<a id="s1-3"></a>

### 1-3. 오늘 배우는 세 프로젝트의 차이

[↑ 목차로 이동](#toc)

| 항목 | 05 Weather MCP (Stateless) | Mini Agent 01 LLM | 06 Stateful Weather |
| --- | --- | --- | --- |
| Compose 파일 | `compose.yml` 1개 | `compose.yml` 1개 | `compose.infrastructure.yml` + `compose.application.yml` 2개 |
| 컨테이너 | frontend, backend, weather-mcp | frontend, backend (필요 시 MCP) | 위 3개 + PostgreSQL + Redis |
| GitHub Workflow 파일 | `07-weather-mcp-cicd.yml` | `mini-agent-01-llm-cicd.yml` | `07-weather-stateful-cicd.yml` |
| EC2 배포 폴더 | `~/weather-mcp-deployment` | workflow가 지정한 폴더 (확인법: C-6) | `~/weather-stateful` |
| EC2 환경 파일 | `.env` | `.env.docker` (수업 기준) | `.env` |
| 백엔드 테스트 | `backend/test_app.py` | `backend/test/test_api.py` | `backend/test_app.py` |

---

<a id="s2"></a>

## 2. 반드시 지킬 핵심 규칙 6가지

[↑ 목차로 이동](#toc)

1. 개발용 `.env` 와 Docker/배포용 환경 파일(`.env.docker`)을 분리한다. `.env` 를 Docker용으로 덮어쓰면 로컬 개발이 망가진다 (`.env` 에는 `127.0.0.1` 같은 로컬 주소가 들어 있다).
2. 컨테이너끼리 부를 때는 `127.0.0.1` 이 아니라 compose.yml 에 적은 서비스 이름(`backend`, `weather-mcp`, `database`, `redis`)을 쓴다.
3. 코드와 compose.yml 은 고정하고, 서버마다 다른 값은 환경 파일만 바꾼다. compose.yml 에는 `${변수:-기본값}` 형태를 쓴다.
4. GitHub에 올리기 전에 로컬에서 먼저 CI 명령(테스트 → `config` → `build`)을 통과시킨다.
5. 환경 파일(API 키 포함)은 Git에 올리지 않는다. 그래서 서버에는 자동으로 생기지 않으므로 **서버에 직접 폴더를 만들고 넣어야 한다.** 배포 오류 1순위 원인이다.
6. 인프라(DB, Redis)를 먼저 띄우고, 그다음 애플리케이션을 띄운다.

---

<a id="part-a"></a>

# Part A. 한 번만 하는 준비

[↑ 목차로 이동](#toc)

<a id="a-1"></a>

## A-1. [내 PC] 도구 확인

[↑ 목차로 이동](#toc)

```powershell
# Docker Desktop을 먼저 실행해 두세요 (고래 아이콘이 떠 있어야 함)
docker version                 # 버전이 출력되면 정상
docker compose version         # compose 버전이 출력되면 정상
git --version                  # git 설치 확인
python --version               # python 설치 확인 (CI는 Python 3.12 사용)
```

<a id="a-2"></a>

## A-2. [GitHub 웹] 저장소와 Workflow 파일 위치 확인

[↑ 목차로 이동](#toc)

- Workflow 파일은 **Git 저장소 맨 위(루트)** 의 `.github/workflows/` 폴더에 있어야 GitHub가 인식합니다. 프로젝트 폴더 안에 두면 동작하지 않습니다.
- Workflow 파일이 없으면 강사가 디스코드에 올린 파일을 아래 위치에 복사합니다.

```text
.github/
└── workflows/
    ├── 07-weather-mcp-cicd.yml         # 05용
    ├── 07-weather-stateful-cicd.yml    # 06용
    └── mini-agent-01-llm-cicd.yml      # Mini Agent 01 LLM용
```

<a id="a-3"></a>

## A-3. [AWS 웹] EC2 서버 만들기 (05에서 이미 만들었다면 건너뛰기)

[↑ 목차로 이동](#toc)

AWS 콘솔 → EC2 → Instances → Launch instances 에서 아래 값으로 만듭니다. 화면은 계정·시점에 따라 조금씩 다를 수 있으며, 수업에서 지정한 Region과 비용 한도가 우선입니다.

| 항목 | 입력값 |
| --- | --- |
| Region | Seoul `ap-northeast-2` (수업 지정값) |
| Name | `weather-mcp-deployment` |
| AMI | Ubuntu Server 24.04 LTS x86_64 (화면에서 직접 선택. 다른 곳의 AMI ID를 복사하지 않기) |
| Instance Type | `t3.small` |
| Root EBS | `16 GiB gp3` |
| Key Pair | 새로 만들거나 지정된 것 선택 후 `.pem` 파일 안전하게 보관 |
| VPC | `(default)` 표시된 것. 없으면 VPC 콘솔 → Actions → Create default VPC |
| Public IPv4 | Enable |
| Security Group (Inbound) | SSH `22` = My IP, Streamlit `8501` = My IP |

- 포트 `8000`(백엔드), `8010`(MCP), `5432`(PostgreSQL), `6379`(Redis)는 **인터넷에 열지 않습니다.**
- 생성 후 Public IPv4 또는 Public DNS를 메모해 둡니다. (Private IP `172.31.x.x` 는 사용하지 않습니다.)
- Key 파일(`.pem`)은 Git, 메신저, README에 올리지 않습니다.

<a id="a-4"></a>

## A-4. [내 PC → EC2] SSH 접속과 Docker 설치

[↑ 목차로 이동](#toc)

```powershell
# [내 PC] 변수에 내 값을 넣습니다 (본인 pem 경로와 EC2 주소로 바꾸기)
$keyPath = "C:\mini\weather-mcp-key.pem"
$server  = "ubuntu@<PUBLIC_IPV4_OR_DNS>"

# [내 PC] EC2 접속 (처음 접속하면 fingerprint 질문에 yes 입력)
ssh -i $keyPath $server
```

`UNPROTECTED PRIVATE KEY FILE` 오류가 나면 pem 파일 권한을 좁혀야 합니다. (자료에는 명령이 없어 일반적인 방법을 적었습니다.)

```powershell
# [내 PC] 상속 권한 제거 후 현재 사용자에게만 읽기 권한 부여
icacls $keyPath /inheritance:r
icacls $keyPath /grant:r "$($env:USERNAME):R"
```

접속에 성공하면 EC2 터미널에서 Docker를 설치합니다. (Amazon Linux를 썼다면 `ec2-user` 와 `yum` 명령을 사용해야 하며, 이 문서는 Ubuntu 기준입니다.)

```bash
# [EC2] 패키지 목록 갱신
sudo apt update
# [EC2] Docker, Compose, Git, curl 설치
sudo apt install -y docker.io docker-compose-v2 git curl
# [EC2] Docker를 켜고, 서버 재부팅 후에도 자동 실행되게 설정
sudo systemctl enable --now docker
# [EC2] sudo 없이 docker 명령을 쓸 수 있도록 ubuntu 사용자를 docker 그룹에 추가
sudo usermod -aG docker ubuntu
# [EC2] 그룹 적용을 위해 접속 종료 (다시 접속해야 적용됨)
exit
```

```powershell
# [내 PC] 다시 접속
ssh -i $keyPath $server
```

```bash
# [EC2] 설치 확인
docker info                          # 에러 없이 정보가 나오면 정상
docker compose version               # 버전이 나오면 정상
docker run --rm hello-world          # "Hello from Docker!" 가 나오면 준비 완료
```

<a id="a-5"></a>

## A-5. [GitHub 웹] production Environment 와 Secret 4개 등록

[↑ 목차로 이동](#toc)

CD가 EC2에 접속할 때 쓰는 정보를 GitHub에 안전하게 저장하는 단계입니다.

1. GitHub 저장소 → `Settings` → `Environments` → `New environment`
2. 이름을 정확히 `production` 으로 생성
3. 가능하면 `Required reviewers` 에 승인자를 지정하고, Deployment branch 를 `main` 으로 제한
4. `Environment secrets` 에 아래 4개 등록

| Secret 이름 | 넣을 값 |
| --- | --- |
| `AWS_HOST` | EC2 Public DNS 또는 Public IPv4 |
| `AWS_USER` | Ubuntu는 `ubuntu` (Amazon Linux는 `ec2-user`) |
| `AWS_SSH_PRIVATE_KEY` | `.pem` 파일을 메모장으로 열어 `-----BEGIN` 부터 `-----END` 줄까지 **전체 복사** (따옴표 추가 금지) |
| `AWS_SSH_KNOWN_HOSTS` | 아래 명령으로 뽑은 **한 줄 전체** |

`AWS_SSH_KNOWN_HOSTS` 값 만들기 (A-4에서 SSH 접속에 성공했어야 결과가 나옵니다):

```powershell
# [내 PC] 접속 기록에서 ssh-ed25519 줄만 뽑아 화면에 출력하고 클립보드에 복사
$knownHost = ssh-keygen -F <PUBLIC_IPV4_OR_DNS> `
  -f "$env:USERPROFILE\.ssh\known_hosts" |
  Select-String "ssh-ed25519" |
  ForEach-Object { $_.Line }

$knownHost                 # 화면에서 내용 확인
$knownHost | Set-Clipboard # 클립보드에 복사 → GitHub Secret 입력칸에 붙여넣기
```

- 등록할 값의 모양: `<서버주소> ssh-ed25519 AAAAC3Nza...(아주 긴 문자열)` 한 줄.
- 등록하면 안 되는 것: `SHA256:...` 지문만 있는 값, `# Host ... found` 주석 줄, `StrictHostKeyChecking=no` 설정.
- 결과가 비어 있으면 이 PC에서 그 주소로 접속한 적이 없거나 IP가 바뀐 것이므로 SSH로 한 번 접속한 뒤 다시 실행합니다.
- **저장소가 다르면 Environment/Secret 도 저장소마다 따로 등록**해야 합니다. 같은 EC2를 쓰면 값은 동일합니다.
- EC2를 새로 만들거나 Stop/Start 후 Public IP가 바뀌면 `AWS_HOST` 와 `AWS_SSH_KNOWN_HOSTS` 를 둘 다 새 주소로 갱신합니다.

<a id="a-6"></a>

## A-6. 주의: GitHub Runner 가 EC2 의 SSH(22)에 들어올 수 있어야 CD 가 됩니다

[↑ 목차로 이동](#toc)

현재 실습 Workflow는 GitHub의 서버(Runner)가 EC2의 SSH 22번 포트로 직접 접속하는 단순 구조입니다. Security Group이 `My IP/32` 만 허용하면 Runner 는 접속하지 못하고 `SSH timeout` 이 납니다.

첫 CD 확인 때만 아래 순서를 사용하고, **끝나면 즉시 원복**합니다. (상시 `0.0.0.0/0` 유지는 금지)

```text
[AWS 웹] Security Group의 SSH 22 Source 를 Anywhere-IPv4(0.0.0.0/0) 로 임시 변경
→ [GitHub] CD 실행 (배포·Health·화면 확인)
→ [AWS 웹] SSH 22 Source 를 My IP/32 로 즉시 복구
```

---

<a id="part-b"></a>

# Part B. 실습 1 — 05 Weather MCP (Stateless, Compose 1개)

[↑ 목차로 이동](#toc)

구성: Browser → Frontend(:8501) → Backend(:8000) → Weather MCP(:8010, 내부 전용) → Open-Meteo / OpenAI 또는 Gemini

<a id="b-1"></a>

## B-1. [내 PC] 환경 파일 만들기

[↑ 목차로 이동](#toc)

```powershell
# 05 프로젝트 폴더로 이동 (본인 경로에 맞게)
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project

# 예시 파일을 복사해 실제 환경 파일 만들기
Copy-Item .env.example .env

# 8000, 8501 포트를 이미 쓰는 프로그램이 있는지 확인 (출력이 없으면 정상)
Get-NetTCPConnection -LocalPort 8000,8501 -ErrorAction SilentlyContinue
# 출력이 있으면 docker ps 로 어떤 컨테이너인지 확인 후, 이 프로젝트의 것일 때만 중지
docker ps
```

`.env` 파일을 열어 API 키를 입력합니다. 사용할 Provider 것만 넣어도 됩니다.

```ini
OPENAI_API_KEY=여기에_OpenAI_키
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=여기에_Gemini_키
GEMINI_MODEL=gemini-3.5-flash
```

```powershell
# .env 가 Git 에 올라가지 않는지 확인 (".env" 라고 출력되면 무시 대상이라 안전)
git check-ignore .env
```

<a id="b-2"></a>

## B-2. [내 PC] 로컬에서 실행해 보기

[↑ 목차로 이동](#toc)

```powershell
# 1) compose.yml 문법 검사 (아무 출력 없이 끝나면 정상, 컨테이너는 만들지 않음)
docker compose config --quiet

# 2) 이미지 빌드 + 컨테이너 백그라운드 실행
docker compose up -d --build

# 3) 상태 확인: 세 서비스가 Up, healthy 여야 정상
docker compose ps
```

기대하는 시작 순서: `weather-mcp` 시작 → Health 통과 → `backend` 시작 → Health 통과 → `frontend` 시작. Frontend 가 안 뜨면 Backend Health 부터 확인합니다.

접속 주소:

| 대상 | 주소 |
| --- | --- |
| 화면(Frontend) | http://127.0.0.1:8501 |
| 백엔드 API 문서 | http://127.0.0.1:8000/docs |
| 백엔드 준비 상태 | http://127.0.0.1:8000/health/ready |

```powershell
# 백엔드 프로세스가 살아있는지
Invoke-RestMethod http://127.0.0.1:8000/health/live
# MCP 도구까지 사용할 준비가 되었는지
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

```powershell
# 화면 없이 API 로 직접 날씨 에이전트 호출 (openai 대신 gemini 도 가능)
$body = @{
    city = "서울"
    day = "tomorrow"
    provider = "openai"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/api/weather `
    -ContentType "application/json" `
    -Body $body
```

브라우저 확인 순서: `http://127.0.0.1:8501` → 왼쪽 메뉴 `Weather Agent` → 도시 `서울`, 날짜 `내일`, Provider 선택 → **실제 날씨 조회** 클릭 → 최종 답변과 `get_weather` Tool Result(기온·강수 확률)가 함께 나오면 성공.

```powershell
# 코드나 .env 를 수정했다면 컨테이너를 새로 만들어서 반영
docker compose up -d --build --force-recreate backend frontend weather-mcp

# 로그 보기 (최근 100줄)
docker compose logs --tail=100 weather-mcp backend frontend
# 특정 컨테이너 로그 계속 보기 (Ctrl+C 로 로그 보기만 종료, 컨테이너는 계속 실행)
docker compose logs -f backend

# 확인이 끝나면 중지 (다음 단계 전에 꼭!)
docker compose down
```

<a id="b-3"></a>

## B-3. [내 PC] 로컬에서 CI 명령 미리 실행 (= 로컬 CI)

[↑ 목차로 이동](#toc)

GitHub에 올리기 전에 GitHub가 할 일과 똑같은 검사를 내 PC에서 먼저 합니다. 로컬에서 실패하는 것을 GitHub에 올리면 원인 찾기가 더 어렵습니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project

# 파이썬 가상환경 만들기 (프로젝트별 패키지 분리) - 이미 있으면 생략
python -m venv .venv
# 가상환경 켜기 (프롬프트 앞에 (.venv) 가 붙으면 성공)
.\.venv\Scripts\Activate.ps1

# pip 최신화 → 백엔드 패키지 설치 → 테스트 도구 설치
python -m pip install --upgrade pip
python -m pip install -r .\backend\requirements.txt
python -m pip install pytest

# 백엔드 테스트 실행 (모두 passed 가 나와야 함)
python -m pytest .\backend\test_app.py -q

# Compose 문법 검사 + 이미지 빌드
docker compose config --quiet
docker compose build
```

`docker compose` 는 가상환경 안에 설치하는 것이 아니라 Docker Desktop 에 요청하는 명령이므로 같은 터미널에서 그대로 실행하면 됩니다.

세 단계(테스트 → config → build)가 모두 성공하면 **로컬 CI 성공**입니다.

> CI 테스트는 실제 OpenAI/Gemini/Open-Meteo 대신 가짜(Fake) 응답을 씁니다. GitHub의 검사용 서버에는 내 PC의 `.env` 와 API 키가 없기 때문입니다. 따라서 CI 성공이 실제 연동 성공을 뜻하지는 않으며, 실제 연동은 로컬과 EC2 화면에서 따로 확인합니다.

<a id="b-4"></a>

## B-4. [내 PC → GitHub] 개인 브랜치에 push 해서 CI 확인

[↑ 목차로 이동](#toc)

```powershell
# Git 저장소 최상위 폴더로 이동 (프로젝트 폴더가 아니라 .github 폴더가 있는 곳)
cd C:\aidevs

# 개인 브랜치 만들기 (main 에 바로 올리지 않기)
git switch -c weather-mcp-lab

# 프로젝트 폴더와 workflow 파일만 골라서 추가
git add 07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project
git add .github/workflows/07-weather-mcp-cicd.yml

# 올라갈 파일 목록 확인 (.env 가 목록에 있으면 안 됨!)
git status

git commit -m "Add weather MCP deployment lab"
git push -u origin weather-mcp-lab
```

[GitHub 웹] 저장소 → `Actions` 탭 → **07 Weather MCP CI CD** → 방금 실행 → `test-and-build` 클릭.

- 개인 브랜치와 Pull Request 에서는 CI만 실행되고 **AWS 배포는 실행되지 않는 것이 정상**입니다.
- 실패하면 마지막 줄이 아니라 **처음 빨간색이 된 Step 의 첫 오류**부터 봅니다.

| 실패한 Step | 먼저 볼 것 |
| --- | --- |
| Install dependencies | Python 버전, requirements 경로·패키지명 |
| Test backend contract | 최초로 실패한 테스트 (로컬 pytest 로 재현) |
| Validate Compose | YAML 들여쓰기, 환경 변수, 파일 경로 |
| Build three images | Dockerfile 의 `COPY` 경로, Base Image |

고친 뒤 새 커밋을 push 하면 새 CI 실행이 생깁니다. (이전 실패 기록이 성공으로 바뀌지는 않습니다.)

<a id="b-5"></a>

## B-5. [내 PC → EC2] 서버에 환경 파일(.env) 넣기

[↑ 목차로 이동](#toc)

Git에는 `.env` 가 없으므로 **서버에 직접** 넣어야 합니다. 이 단계를 빼먹으면 CD가 `.env` 없음 오류로 실패합니다.

```powershell
# [내 PC] 변수 준비 (A-4에서 만든 것과 동일)
$keyPath  = "C:\mini\weather-mcp-key.pem"
$server   = "ubuntu@<PUBLIC_IPV4_OR_DNS>"
$localEnv = "C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project\.env"

# 로컬 .env 가 실제로 있는지 확인 (True 가 나와야 함)
Test-Path $localEnv

# 서버에 배포 폴더 만들기
ssh -i $keyPath $server "mkdir -p ~/weather-mcp-deployment"

# .env 한 파일만 서버로 전송 (프로젝트 전체나 .venv 는 보내지 않기)
scp -i $keyPath $localEnv "${server}:~/weather-mcp-deployment/.env"

# 소유자만 읽도록 권한 설정 후 확인 (-rw------- 로 보이면 정상)
ssh -i $keyPath $server "chmod 600 ~/weather-mcp-deployment/.env && ls -l ~/weather-mcp-deployment/.env"
```

직접 입력하고 싶다면 (위 scp 대신):

```bash
# [EC2] 폴더 만들고 .env 직접 작성
mkdir -p ~/weather-mcp-deployment
cd ~/weather-mcp-deployment
nano .env          # 아래 4줄 입력 후 Ctrl+O, Enter, Ctrl+X 로 저장
chmod 600 .env     # 소유자만 읽기/쓰기
```

```ini
OPENAI_API_KEY=<실제 OpenAI API Key>
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=<실제 Gemini API Key>
GEMINI_MODEL=gemini-3.5-flash
```

`cat .env` 결과를 화면 공유하거나 로그에 출력하지 않습니다.

<a id="b-6"></a>

## B-6. [GitHub 웹] main 병합 → 승인 → 자동 배포 (CD)

[↑ 목차로 이동](#toc)

1. 개인 브랜치 push 후 나타나는 `Compare & pull request` 로 Pull Request 를 만들고 CI 통과를 확인합니다.
2. 검토 후 `main` 에 Merge 합니다.
3. `Actions` → **07 Weather MCP CI CD** 에서 `main` 실행을 엽니다.
4. CI 가 성공하면 deploy 잡이 `Waiting` 상태가 됩니다 → `Review deployments` → `production` 체크 → `Approve and deploy`.
5. 승인 기능이 없는 요금제라면 승인 없이 바로 실행될 수 있습니다.

<a id="b-7"></a>

## B-7. 배포 결과 확인

[↑ 목차로 이동](#toc)

```text
브라우저: http://<EC2_PUBLIC_IP>:8501
```

```bash
# [EC2] 서버에서도 확인
cd ~/weather-mcp-deployment
docker compose ps                                              # 세 서비스 Up / healthy 확인
docker compose logs --tail=100 weather-mcp backend frontend    # 최근 로그
curl --fail http://127.0.0.1:8000/health/live                  # 백엔드 생존 확인
curl --fail http://127.0.0.1:8000/health/ready                 # MCP 연결까지 준비 확인
```

화면에서 **실제 날씨를 한 번 조회해 Tool Result 와 LLM 답변까지 확인**해야 배포 완료입니다. 컨테이너가 `Up` 이라는 것만으로 성공이라고 판단하지 않습니다.

---

<a id="part-c"></a>

# Part C. 실습 2 — Mini Agent 01 LLM 프로젝트를 CI/CD 로 배포 (수업 시연)

[↑ 목차로 이동](#toc)

Part B 와 같은 방식을 다른 프로젝트에 적용하는 실습입니다. 흐름은 다음과 같습니다.

```text
Docker Compose 구성 → 백엔드 테스트 → 로컬 CI(config, build) → Workflow 준비 → GitHub 설정 → push → CD
```

<a id="c-1"></a>

## C-1. [내 PC] 프로젝트에 있어야 하는 파일 확인

[↑ 목차로 이동](#toc)

```text
mini_agent/                              # Git 저장소 루트 (본인 폴더명에 맞게)
├── compose.yml                          # 프론트/백엔드(/MCP) 실행 방법 정의
├── .dockerignore                        # 이미지에 넣지 않을 파일 목록
├── .env                                 # 개발용 (로컬 주소 127.0.0.1) - 건드리지 않기
├── .env.docker                          # Compose/배포용 (서비스 이름 주소) - Git 제외
├── .env.example                         # .env 예시 (키 값 없이) - Git 포함
├── .env.docker.example                  # .env.docker 예시 (키 값 없이) - Git 포함
├── requirements.txt                     # 프로젝트 루트의 requirements
├── backend/
│   ├── Dockerfile                       # 백엔드 실행 스크립트
│   └── test/
│       └── test_api.py                  # 백엔드 API 테스트 프로그램
├── frontend/
│   └── Dockerfile                       # 프론트엔드 실행 스크립트
└── .github/workflows/
    └── mini-agent-01-llm-cicd.yml       # CI/CD 정의 (강사 제공 파일)
```

- `compose.yml` 과 `.dockerignore` 가 없으면 강사가 제공한 파일을 참고해서 만듭니다.
- `.dockerignore` 는 Docker 빌드에 포함하지 않을 파일을 지정합니다.
- 수업 전사본에서 환경 파일명이 명확하지 않게 인식되었습니다. 이 문서는 `.env.docker` 로 통일합니다. 본인 프로젝트의 `compose.yml` 의 `env_file:` 이름과 반드시 같게 맞추세요.

<a id="c-2"></a>

## C-2. [내 PC] 개발용 .env 와 Compose용 환경 파일 분리

[↑ 목차로 이동](#toc)

```powershell
# 프로젝트 루트로 이동 (본인 경로로 바꾸기)
cd <mini_agent 프로젝트 폴더>

# 개발용 .env 는 그대로 두고, 복사해서 Docker용 파일을 만든다 (.env 를 덮어쓰지 않기!)
Copy-Item .env .env.docker
```

`.env.docker` 를 열어 아래 원칙대로 수정합니다.

```ini
# 예시입니다. 변수 이름은 본인 프로젝트의 .env 에 있는 이름을 그대로 쓰고, 값만 바꾸세요.
# 1) 주소는 127.0.0.1 대신 compose.yml 에 정의한 서비스 이름으로 바꿉니다.
BACKEND_URL=http://backend:8000
# 2) 빠져 있는 키/모델 값이 있으면 채웁니다.
OPENAI_API_KEY=여기에_OpenAI_키
GEMINI_API_KEY=여기에_Gemini_키
GEMINI_MODEL=<사용할 모델명>
# 3) Ollama(로컬 LLM) 설정은 AWS 배포에서 실행되지 않으므로 신경 쓰지 않습니다.
```

```powershell
# 다른 사람이 프로젝트를 실행할 수 있게 "키 값 없는 예시 파일"을 만든다
Copy-Item .env .env.example
Copy-Item .env.docker .env.docker.example
# → 두 예시 파일을 열어서 실제 API 키 값은 지우고 항목 이름만 남기세요.

# .env 와 .env.docker 가 Git 무시 대상인지 확인 (파일명이 출력되면 안전)
git check-ignore -v .env .env.docker
```

`compose.yml` 안에서 아래 항목을 확인합니다.

```yaml
# backend / frontend 서비스마다 확인할 것 (예시 모양)
build:
  dockerfile: backend/Dockerfile      # 1) Dockerfile 위치가 맞는지
env_file:
  - .env.docker                       # 2) 환경 파일 이름이 정확한지 (.env 이면 지정 없이도 자동 인식)
ports:
  - "8000:8000"                       # 3) 포트 연결이 맞는지
# 4) 서비스 이름(backend, frontend 등)이 환경 파일의 주소 이름과 일치하는지
# 5) 필요하면 image: 로 이미지 이름을 직접 지정 가능 (안 쓰면 "프로젝트명-서비스명" 으로 자동 생성)
```

`.env` 가 아닌 다른 이름을 쓰면 실행 명령에서 지정해야 할 수 있습니다.

```powershell
# 환경 파일 이름이 .env 가 아닐 때 직접 지정하는 방법 (compose.yml 에 env_file 이 있다면 생략 가능)
docker compose --env-file .env.docker up
```

<a id="c-3"></a>

## C-3. [내 PC] 백엔드 테스트 프로그램 준비

[↑ 목차로 이동](#toc)

백엔드는 배포 전에 **만든 사람이 직접 테스트**해야 합니다. 테스트하지 않은 코드가 서버에 올라가면 장애로 이어집니다.

테스트 케이스는 성공 사례만 만들면 안 됩니다.

| 종류 | 확인 내용 |
| --- | --- |
| Happy case | 올바른 입력에 정상 응답하는가 |
| Unhappy case | 잘못된 입력·오류 상황을 제대로 처리하는가 |
| 예외 케이스 | 필수 값 누락, 형식 오류 |
| 비정상 케이스 | 예상 못한 요청 |

URL 하나에 테스트 케이스가 보통 5개쯤 필요합니다. 테스트 파일을 직접 만들기 어려우면 Codex 에 아래처럼 위치를 명확히 지정해 요청하고, 생성된 코드가 내 폴더 구조와 API 경로에 맞는지 반드시 확인하세요.

```text
[Codex 에 붙여넣을 요청 예시]
backend 폴더 아래 test 폴더에 test_api.py 라는 테스트 프로그램을 작성해줘.
백엔드의 모든 API URL 에 대해 정상 / 예외 / 비정상 케이스를 pytest 로 검증해줘.
```

<a id="c-4"></a>

## C-4. [내 PC] 로컬 테스트 실행

[↑ 목차로 이동](#toc)

```powershell
# 프로젝트 루트에서 가상환경 켜기
.\.venv\Scripts\Activate.ps1

# pip 업그레이드
python -m pip install --upgrade pip
# 프로젝트 루트의 requirements.txt 설치 (backend 폴더 안의 것이 아님!)
pip install -r requirements.txt
# 테스트 도구 설치
pip install pytest

# workflow 의 working-directory 와 같은 기준으로 backend 폴더에서 테스트 실행
cd backend
python -m pytest test/test_api.py -q
# 기대 결과: 수업에서는 "19 passed" 처럼 전부 통과 (100%)
cd ..
```

MCP 서버가 있는 프로젝트라면 MCP 서버용 테스트도 별도로 준비해 실행합니다.

<a id="c-5"></a>

## C-5. [내 PC] 로컬 CI: Compose 검사와 이미지 빌드

[↑ 목차로 이동](#toc)

```powershell
# 프로젝트 루트에서 실행
# 1) compose.yml 문법 검사 (YAML 오류, 서비스명 오타, 환경파일 경로, 포트, Dockerfile 경로 오류를 잡아줌)
docker compose config

# 2) 프론트엔드/백엔드 이미지 빌드
docker compose build
```

```text
pytest 통과 → docker compose config 통과 → docker compose build 성공
= 로컬 CI 성공
```

<a id="c-6"></a>

## C-6. [내 PC] Workflow 파일 확인 (수정할 곳 3군데)

[↑ 목차로 이동](#toc)

`.github/workflows/mini-agent-01-llm-cicd.yml` 이 없으면 강사가 올린 파일을 그 위치에 복사한 뒤 아래 세 가지를 확인합니다.

```powershell
# workflow 파일에서 확인할 줄들을 한 번에 찾기
Select-String -Path .github\workflows\mini-agent-01-llm-cicd.yml -Pattern "branches|working-directory|environment|cd "
```

| 확인 항목 | 올바른 상태 |
| --- | --- |
| 실행 조건 `on:` | `push` 의 `branches: - main` (main 에 push 될 때만 CI/CD 실행). 팀 정책상 Pull Request 때는 실행하기 싫다면 `pull_request` 조건을 삭제 |
| `working-directory` | 실제 테스트 위치와 일치 (예: `backend`). CI 오류의 흔한 원인이 코드가 아니라 **잘못된 폴더에서 명령을 실행**하는 것 |
| `environment` | 배포 Job 의 `environment:` 값이 GitHub 에 등록한 이름과 같아야 함. Part A-5 에서 만든 `production` 을 재사용하려면 `environment: production` 으로 맞춤 |
| 서버 배포 폴더 | CD 단계의 `cd <폴더>` 등에 적힌 서버 폴더 이름 → 다음 단계 C-8 에서 서버에 만들 폴더 |

```yaml
# 참고: 실행 조건 예시
on:
  push:
    branches:
      - main

# 참고: 테스트 폴더 기준을 지정하는 두 가지 방법
defaults:
  run:
    working-directory: backend
# 또는 단계마다
- name: Run tests
  run: pytest
  working-directory: backend
```

<a id="c-7"></a>

## C-7. [GitHub 웹] Environment / Secret 확인

[↑ 목차로 이동](#toc)

- 이 프로젝트의 GitHub 저장소 → `Settings` → `Environments` 에 `production` 과 Secret 4개(`AWS_HOST`, `AWS_USER`, `AWS_SSH_PRIVATE_KEY`, `AWS_SSH_KNOWN_HOSTS`)가 있어야 합니다. 없으면 Part A-5 를 그대로 수행합니다.
- 수업에서는 같은 EC2·같은 pem 을 재사용했으므로 값은 기존과 동일합니다. **다른 서버에 배포하고 싶을 때만** 새 Environment 를 추가합니다.

<a id="c-8"></a>

## C-8. [EC2] 서버에 배포 폴더와 환경 파일 미리 만들기 (오류 예방)

[↑ 목차로 이동](#toc)

수업에서는 이 단계를 하지 않아 배포가 실패했습니다.

```text
Git에는 코드와 compose.yml 만 있음, .env.docker 는 없음
→ 서버에서 Compose 가 필요한 환경 변수를 못 읽음 → 배포 실패
```

```bash
# [EC2] 서버에 어떤 폴더가 있는지 먼저 확인 (처음에는 아무것도 없음)
ls
# workflow 의 배포 폴더 이름과 정확히 같은 폴더 만들기 (이름은 자유지만 workflow 와 일치해야 함)
mkdir -p <배포폴더>
```

```powershell
# [내 PC] .env.docker 를 서버의 배포 폴더로 복사
$keyPath = "C:\mini\weather-mcp-key.pem"
$server  = "ubuntu@<PUBLIC_IPV4_OR_DNS>"
scp -i $keyPath .env.docker "${server}:~/<배포폴더>/.env.docker"
ssh -i $keyPath $server "chmod 600 ~/<배포폴더>/.env.docker && ls -la ~/<배포폴더>"
```

```text
서버 결과 모양:
<배포폴더>/
└── .env.docker
```

<a id="c-9"></a>

## C-9. [내 PC → GitHub] main 에 push 해서 CI/CD 실행

[↑ 목차로 이동](#toc)

```powershell
# 프로젝트(저장소) 루트에서 실행
git status                      # .env, .env.docker 가 올라가는 목록에 있으면 안 됨!
git add .
git commit -m "Add Docker Compose CI/CD"
git push origin main
```

[GitHub 웹] 저장소 → `Actions` → 방금 push 로 시작된 workflow(`mini-agent-01-llm-cicd.yml`) 실행 클릭

```text
CI 가 먼저 실행 (Python 설치 → pip 업그레이드 → requirements 설치 → pytest → compose 검증 → 이미지 빌드)
→ 성공하면 CD 실행 (SSH 로 EC2 접속 → 배포 폴더 이동 → 환경 파일 확인 → docker compose up -d)
```

- 에러가 나면 **처음 빨간색이 된 Step 의 로그**를 봅니다. 배포 단계 오류의 1순위는 코드가 아니라 **환경 파일 존재 여부 → 파일 경로 → working-directory → 서버 배포 폴더** 순으로 확인하는 것입니다.
- 서버에 폴더와 환경 파일을 넣은 뒤에는 다시 push 하거나 Actions 에서 실패한 실행의 `Re-run jobs` 로 재실행합니다.

```bash
# [EC2] 배포 후 확인
cd ~/<배포폴더>
docker compose ps        # 컨테이너 Up 확인
docker ps                # 전체 컨테이너 확인
```

---

<a id="part-d"></a>

# Part D. 실습 3 — 06 Stateful Weather (인프라와 애플리케이션 분리)

[↑ 목차로 이동](#toc)

05 에 **PostgreSQL(완료 이력 영구 저장)** 과 **Redis(진행 상태·날씨 캐시)** 를 추가한 프로젝트입니다.

```text
Browser → Frontend → Backend Agent → Weather MCP → Open-Meteo
                         ├→ Redis: 진행 상태·날씨 Cache (600초)
                         ├→ PostgreSQL: 완료 실행 이력
                         └→ OpenAI 또는 Gemini
```

| 구분 | 05 Stateless | 06 Stateful |
| --- | --- | --- |
| 진행 상태 | 저장 안 함 | Redis 저장, Frontend 가 주기적으로 조회 |
| 같은 날씨 재조회 | 매번 MCP 호출 | Redis 캐시 사용 |
| 완료 이력 | 저장 안 함 | PostgreSQL 영구 저장 |
| Compose | 1개 | 인프라 / 애플리케이션 2개 |
| 재배포 | 전체 재실행 | **앱만 교체, 데이터 유지** |

핵심 원칙: **인프라(DB·Redis)는 한 번 띄워 두고, 애플리케이션만 반복 배포**합니다. 인프라가 먼저 떠 있어야 백엔드가 연결할 수 있습니다.

<a id="d-1"></a>

## D-1. [내 PC] 06 환경 파일 만들기

[↑ 목차로 이동](#toc)

```powershell
# 05 컨테이너가 로컬에서 실행 중이면 먼저 중지 (05와 06은 8000, 8501 포트를 같이 씀)
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project
docker compose down

# 06 프로젝트로 이동
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment

# 환경 파일 만들기
Copy-Item .env.example .env
```

`.env` 에 키를 입력합니다. 아래 내부 주소의 `database`, `redis`, `weather-mcp` 는 Compose 서비스 이름이므로 `127.0.0.1` 로 바꾸지 않습니다.

```ini
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash

# 아래 3줄은 서비스 이름으로 연결하는 값. 127.0.0.1 로 바꾸면 자기 자신을 가리켜 연결 실패
DATABASE_URL=postgresql://agent_user:agent_pwd@database:5432/agent_db
REDIS_URL=redis://redis:6379/0
WEATHER_MCP_URL=http://weather-mcp:8010/mcp
WEATHER_CACHE_TTL_SECONDS=600
```

```powershell
# .env 가 Git 무시 대상인지 확인
git check-ignore .env
```

<a id="d-2"></a>

## D-2. [내 PC] 1단계 — 인프라(PostgreSQL, Redis) 먼저 실행

[↑ 목차로 이동](#toc)

```powershell
# 문법 검사 (출력 없으면 정상)
docker compose -f .\compose.infrastructure.yml config --quiet
# 인프라 실행 (백그라운드)
docker compose -f .\compose.infrastructure.yml up -d
# 상태 확인: database, redis 둘 다 healthy 가 될 때까지 기다린다 (수십 초 소요)
docker compose -f .\compose.infrastructure.yml ps
```

- 처음 실행할 때 **새 PostgreSQL Volume 에만** `database/init.sql` 이 자동 실행되어 `weather_agent.runs` 테이블이 만들어집니다. 이미 만들어진 Volume 에는 다시 실행되지 않습니다.
- 컨테이너가 떴다고 바로 연결 가능한 것은 아니어서 `healthy` 확인(health check)이 필요합니다.

<a id="d-3"></a>

## D-3. [내 PC] 2단계 — 애플리케이션 실행

[↑ 목차로 이동](#toc)

```powershell
# 문법 검사
docker compose -f .\compose.application.yml config --quiet
# 이미지 빌드 + 실행
docker compose -f .\compose.application.yml up -d --build
# 상태 확인
docker compose -f .\compose.application.yml ps
```

`weather-stateful` 네트워크를 찾을 수 없다는 오류가 나면 D-2 인프라를 먼저 실행하지 않은 것입니다.

| 확인 대상 | 주소 |
| --- | --- |
| 화면(Frontend) | http://127.0.0.1:8501 |
| 백엔드 API 문서 | http://127.0.0.1:8000/docs |
| 백엔드 준비 상태 | http://127.0.0.1:8000/health/ready |

```powershell
# 백엔드 생존 / 의존 서비스(MCP, PostgreSQL, Schema, Redis) 준비 상태 확인
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

화면 실습 순서:

1. `http://127.0.0.1:8501` 열기 → 도시 `서울`, 날짜 `내일` 선택
2. 실행 버튼 → 진행 표시줄(Progress Bar)과 현재 단계가 변하는지 확인
3. 최종 답변과 MCP Tool Result 의 온도·강수 정보 비교
4. 실행 이력 화면에서 PostgreSQL 에 저장된 완료 기록 확인
5. **같은 도시·날짜를 다시 실행** → Redis Cache 사용 표시 확인

DB 와 Redis 를 직접 들여다보기:

```powershell
# PostgreSQL 실행 이력 최근 10건 조회
docker compose -f .\compose.infrastructure.yml exec database psql -U agent_user -d agent_db -c "SELECT run_id, city, day, provider, model, created_at FROM weather_agent.runs ORDER BY created_at DESC LIMIT 10;"

# Redis 에 저장된 날씨 관련 Key 조회 (FLUSHALL 은 다른 데이터까지 지우므로 사용 금지)
docker compose -f .\compose.infrastructure.yml exec redis redis-cli --scan --pattern "weather:*"
```

Schema 가 없다는 오류가 나면 (`init.sql` 추가 전에 만든 Volume 인 경우):

```powershell
# init.sql 을 수동으로 적용
Get-Content .\database\init.sql | docker compose -f .\compose.infrastructure.yml exec -T database psql -U agent_user -d agent_db
# 백엔드/프론트엔드 재생성
docker compose -f .\compose.application.yml up -d --build --force-recreate backend frontend
```

코드나 `.env` 를 수정한 뒤에는 앱만 다시 만듭니다. (DB, Redis 컨테이너와 Volume 은 그대로)

```powershell
docker compose -f .\compose.application.yml up -d --build --force-recreate weather-mcp backend frontend
```

로그 확인과 종료:

```powershell
# 애플리케이션 로그 (최근 100줄)
docker compose -f .\compose.application.yml logs --tail=100 weather-mcp backend frontend

# 애플리케이션만 종료 (PostgreSQL, Redis, 데이터는 유지됨)
docker compose -f .\compose.application.yml down

# 실습을 완전히 끝낼 때만 인프라도 종료 (일반 down 은 Volume 유지)
docker compose -f .\compose.infrastructure.yml down

# 주의: down -v 는 PostgreSQL 이력과 Redis 데이터를 영구 삭제합니다 (복구 불가).
# 완전 초기화가 명확히 필요할 때만 사용:
# docker compose -f .\compose.infrastructure.yml down -v
```

<a id="d-4"></a>

## D-4. [내 PC] 로컬 CI 실행

[↑ 목차로 이동](#toc)

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment

python -m venv .venv                                   # 이미 있으면 생략
.\.venv\Scripts\Activate.ps1                           # 가상환경 켜기
python -m pip install --upgrade pip
python -m pip install -r .\backend\requirements.txt
python -m pip install pytest
python -m pytest .\backend\test_app.py -q              # 백엔드 테스트 (Fake MCP·LLM·Store 사용)
docker compose -f .\compose.infrastructure.yml config --quiet    # 인프라 Compose 문법 검사
docker compose -f .\compose.application.yml config --quiet       # 앱 Compose 문법 검사
docker compose -f .\compose.application.yml build                # 앱 이미지 3개만 빌드
```

빌드 대상은 프론트엔드·백엔드·MCP 서버 3개뿐입니다. Redis 와 PostgreSQL 은 이미 공개된 이미지를 받아서 쓰므로 CI 에서 빌드하지 않습니다.

<a id="d-5"></a>

## D-5. [GitHub 웹] 05 Workflow 비활성화, 06 Workflow 활성화

[↑ 목차로 이동](#toc)

05 와 06 은 같은 EC2 의 `8000`, `8501` 포트를 같이 사용합니다. 두 Workflow 가 동시에 배포하면 서로 덮어쓰거나 포트가 충돌하므로 **06 을 시작하기 전에 05 를 비활성화**합니다.

```text
[05 비활성화]
GitHub 저장소 → Actions → 07 Weather MCP CI CD → 오른쪽 위 ··· → Disable workflow

[06 활성화 확인]
Actions → 07 Stateful Weather CI CD
→ "Enable workflow" 버튼이 보이면 클릭 (버튼이 없고 "Run workflow" 가 보이면 이미 활성화됨)
```

- `Disable workflow` 는 파일을 삭제하지 않습니다. 실행만 잠시 멈춥니다.
- Workflow 파일을 삭제하거나 이름을 바꾸는 방식은 쓰지 않습니다.

| 현재 실습 | 05 Workflow | 06 Workflow |
| --- | --- | --- |
| 05 배포 | Enabled | 실행 안 함 |
| 06 배포 | Disabled | Enabled |
| 다시 05 로 전환 | Enabled | Disabled |

<a id="d-6"></a>

## D-6. [내 PC → GitHub] 개인 브랜치에서 CI 확인

[↑ 목차로 이동](#toc)

```powershell
cd C:\aidevs
git switch -c weather-stateful-lab
git add 07_multi-agent-service-ops/00_runtime-and-deployment/06_weather-mcp-stateful-deployment
git add .github/workflows/07-weather-stateful-cicd.yml
git status                                              # .env 가 없는지 확인
git commit -m "Add stateful weather deployment lab"
git push -u origin weather-stateful-lab
```

[GitHub 웹] `Actions` → **07 Stateful Weather CI CD** → 브랜치·커밋 확인 → `test-and-build` 잡 열기.

| 실패 Step | 먼저 확인할 내용 |
| --- | --- |
| Install and test | Python 버전, requirements, 최초 실패 테스트 |
| Validate Compose | YAML 들여쓰기, 환경 변수, 외부 Network 선언 |
| Build application images | Dockerfile 의 Base Image · COPY 경로 |

<a id="d-7"></a>

## D-7. [EC2] 05 → 06 서버 전환 (같은 EC2 재사용)

[↑ 목차로 이동](#toc)

```powershell
# [내 PC] EC2 접속
$keyPath = "C:\mini\weather-mcp-key.pem"
$server  = "ubuntu@<PUBLIC_IPV4_OR_DNS>"
ssh -i $keyPath $server
```

```bash
# [EC2] 05 가 정상 동작 중인지 마지막으로 확인
cd ~/weather-mcp-deployment
docker compose ps
curl --fail http://127.0.0.1:8000/health/ready

# [EC2] 확인이 끝났으면 05 중지 (컨테이너와 전용 네트워크만 제거, 소스와 .env 는 보존)
docker compose down --remove-orphans
# [EC2] 실행 중인 컨테이너가 없는지 확인
docker ps
```

```bash
# [EC2] 서버 자원 확인
free -h               # 메모리: 약 2 GiB(t3.small) 이상이면 진행 가능. 약 1 GiB 면 t3.micro 로 잘못 만든 것
df -h /               # 디스크: 여유 8 GiB 이상이면 진행 가능
docker system df      # Docker 사용량
```

```bash
# [EC2] Docker 정상 동작 재확인 (재설치 불필요)
docker version
docker compose version
docker run --rm hello-world
```

Instance 를 Stop/Start 하면 Public IP 가 바뀔 수 있습니다. 바뀌었다면 다음을 모두 갱신합니다: 로컬 SSH 접속 주소, GitHub production 의 `AWS_HOST`, `AWS_SSH_KNOWN_HOSTS`, 브라우저 주소.

<a id="d-8"></a>

## D-8. [내 PC → EC2] 06 전용 환경 파일 서버에 전송

[↑ 목차로 이동](#toc)

서버에는 06 전용 `.env` 가 있어야 합니다. **이 파일이 없어서 Compose build 가 실패**하는 것이 오늘 수업의 대표 오류였습니다.

```powershell
$keyPath  = "C:\mini\weather-mcp-key.pem"
$server   = "ubuntu@<PUBLIC_IPV4_OR_DNS>"
$localEnv = "C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment\.env"

# 로컬 .env 존재 확인 (True)
Test-Path $localEnv

# 서버에 06 배포 폴더 만들기 (이 폴더 이름은 workflow 가 참조하는 경로와 같아야 함)
ssh -i $keyPath $server "mkdir -p ~/weather-stateful"

# .env 한 파일만 전송
scp -i $keyPath $localEnv "${server}:~/weather-stateful/.env"

# 권한 설정 및 확인 (-rw------- 이면 정상)
ssh -i $keyPath $server "chmod 600 ~/weather-stateful/.env && ls -l ~/weather-stateful/.env"
```

서버의 `.env` 에는 아래 값들이 들어 있어야 합니다. (DB 계정 값은 팀에서 정한 값으로 설정)

```ini
OPENAI_API_KEY=<실제 OpenAI API Key>
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=<실제 Gemini API Key>
GEMINI_MODEL=gemini-3.5-flash
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=agent_pwd
POSTGRES_DB=agent_db
WEATHER_CACHE_TTL_SECONDS=600
```

Workflow 는 서버의 `.env` 를 복사하거나 덮어쓰지 않습니다. API 키와 비밀번호는 화면이나 Actions 로그에 출력하지 않습니다.

<a id="d-9"></a>

## D-9. [GitHub 웹] 최초 자동 배포 (인프라 + 애플리케이션)

[↑ 목차로 이동](#toc)

`production` Environment 와 Secret 4개는 05 와 같은 EC2 라면 그대로 재사용합니다. (Public IP 가 바뀌었으면 `AWS_HOST`, `AWS_SSH_KNOWN_HOSTS` 갱신)

```text
Actions
→ 07 Stateful Weather CI CD
→ Run workflow
→ Use workflow from: main
→ "Deploy 06 infrastructure and application to AWS EC2" 체크 (deploy=true)
→ Run workflow
```

`deploy=false` 로 실행하면 CI 만 돌고 배포는 `Skipped` 됩니다. 배포 Job 이 `Waiting` 이면 `Review deployments → production → Approve and deploy` 로 승인합니다.

| 상태 | 의미 |
| --- | --- |
| `Skipped` | `deploy=false` 이거나 배포 조건 불일치 |
| `Waiting` | `production` 승인 대기 |
| `Queued` | GitHub Runner 할당 대기 |
| `In progress` | 테스트·빌드 또는 EC2 배포 진행 중 |
| `Failure` | 처음 실패한 Step 의 로그 확인 |
| `Success` | Backend Readiness 까지 성공 |

- 자동으로도 실행됩니다: `backend/`, `frontend/`, `mcp_server/`, `database/`, `compose.infrastructure.yml`, `compose.application.yml` 변경을 `main` 에 push 했을 때. README·문서만 바꾼 커밋은 배포가 돌지 않는 것이 정상입니다.
- 첫 배포는 프론트/백엔드/MCP 와 PostgreSQL/Redis 를 모두 설치하므로 오래 걸립니다. 두 번째부터는 빨라집니다.

---

<a id="part-e"></a>

# Part E. 오후 팀 과제 — 초기화 후 스스로 구성해 보기

[↑ 목차로 이동](#toc)

지금까지는 강사가 준 파일을 그대로 실행했습니다. 이제 팀이 직접 Docker Compose 와 CI/CD 를 구성해 봅니다.

<a id="e-1"></a>

## E-1. 기존 실습 환경 정리

[↑ 목차로 이동](#toc)

```bash
# [EC2] 06 앱 컨테이너 중지·삭제
cd ~/weather-stateful
docker compose -f compose.application.yml down --remove-orphans
# [EC2] 인프라 컨테이너 중지·삭제 (일반 down 은 DB 데이터 Volume 유지)
docker compose -f compose.infrastructure.yml down
# 완전 초기화(DB 데이터까지 삭제)가 필요할 때만, 복구 불가:
# docker compose -f compose.infrastructure.yml down -v

# [EC2] 사용하지 않는 이미지·캐시 정리 (질문이 나오면 y)
docker image prune -a

# [EC2] 배포 폴더 삭제 (복구 불가! .env 도 함께 사라지므로 다음 실습 때 다시 넣어야 함)
cd ~
rm -r ~/weather-stateful
# 05 폴더도 지우려면 아래 줄의 맨 앞 # 을 지우고 실행 (05 소스를 복구용으로 남기려면 그대로 두기)
# rm -r ~/weather-mcp-deployment
```

`rm -r` 은 휴지통 없이 바로 삭제됩니다. 폴더 이름을 한 번 더 확인한 뒤 실행하세요.

<a id="e-2"></a>

## E-2. 프로젝트 선택

[↑ 목차로 이동](#toc)

| 프로젝트 | 특징 |
| --- | --- |
| 미니 에이전트 | 비교적 단순, 최소 시간으로 실습 가능. 오늘 한 프로젝트를 그대로 사용해도 됨 |
| MCP 포함 프로젝트 (제로3 MCP) | MCP 서버 2대 + 프론트엔드 + 백엔드. 환경 파일과 테스트 프로그램까지 준비해 CI 성공 후 CD 진행 |

<a id="e-3"></a>

## E-3. 팀 역할 분담 (4명 기준)

[↑ 목차로 이동](#toc)

| 담당 | 할 일 |
| --- | --- |
| 1명 | Redis · 데이터베이스 설치(인프라), 필요하면 CI/CD 전체 담당, **자기 서버의 Public IP 를 팀원에게 공유** |
| 나머지 3명 | 프론트엔드 CI/CD, 백엔드 CI/CD, MCP 서버 CI/CD 각각 담당 |

- 서로 다른 계정의 서버(같은 네트워크 아님)에 접속하려면 Private IP 가 아니라 **Public IP** 를 써야 합니다.
- CI/CD 파이프라인은 팀원 모두가 만들 필요 없습니다. 한 명이 만들고 관리해도 되지만, 익히려면 직접 반복해 보는 것이 가장 좋습니다.
- 직접 만들 때 체크할 것: `compose.yml`(또는 인프라/앱 Compose), `.dockerignore`, 개발용 `.env` 와 Compose용 환경 파일 분리, 테스트 프로그램, Workflow 파일, 서버 배포 폴더와 환경 파일.

---

<a id="part-f"></a>

# Part F. 최종 체크리스트

[↑ 목차로 이동](#toc)

<a id="f-1"></a>

## 로컬 준비

[↑ 목차로 이동](#toc)
- [ ] `compose.yml`(또는 인프라/앱 Compose 2개)이 있고 서비스가 정의되어 있다
- [ ] `.dockerignore` 가 있다
- [ ] 개발용 `.env` 와 Compose용 환경 파일을 분리했다
- [ ] API 키가 든 파일은 Git 에 올라가지 않는다 (`git check-ignore`, `git status` 로 확인)
- [ ] 다른 사람이 참고할 환경 파일 예시(`.env.example` 등)를 만들었다
- [ ] 백엔드 테스트 파일이 있고 정상/예외/비정상 케이스를 다룬다

<a id="f-2"></a>

## 로컬 CI

[↑ 목차로 이동](#toc)
- [ ] `pytest` 가 모두 통과한다
- [ ] `docker compose config` 가 통과한다
- [ ] `docker compose build` 가 성공한다
- [ ] (06) 인프라를 먼저 실행하고 `healthy` 를 확인한 뒤 앱을 실행했다

<a id="f-3"></a>

## GitHub

[↑ 목차로 이동](#toc)
- [ ] `.github/workflows/` 에 CI/CD YAML 이 저장소 루트 기준으로 있다
- [ ] 실행 브랜치·이벤트(`main` push 등)가 팀 정책에 맞다
- [ ] `working-directory` 가 실제 테스트 폴더와 맞다
- [ ] `production` Environment 와 Secret 4개(`AWS_HOST`, `AWS_USER`, `AWS_SSH_PRIVATE_KEY`, `AWS_SSH_KNOWN_HOSTS`)를 설정했다
- [ ] 개인 브랜치와 Pull Request 에서는 배포되지 않음을 확인했다
- [ ] (06) 05 Workflow 를 Disable 하고 06 을 Enable 했다

<a id="f-4"></a>

## AWS 서버

[↑ 목차로 이동](#toc)
- [ ] EC2 에 Docker, Compose 가 설치되어 있고 `hello-world` 가 실행된다
- [ ] 서버에 배포 폴더가 있고, 그 안에 환경 파일이 있다 (권한 `600`)
- [ ] Security Group: SSH 22 와 Streamlit 8501 만 열려 있고 8000, 8010, 5432, 6379 는 닫혀 있다
- [ ] CD 확인 후 SSH 22 를 `My IP/32` 로 원복했다

<a id="f-5"></a>

## 배포 결과

[↑ 목차로 이동](#toc)
- [ ] `main` push (또는 `deploy=true` 수동 실행) 후 Actions 가 성공했다
- [ ] 브라우저 `http://<EC2_PUBLIC_IP>:8501` 에서 실제 날씨 조회와 LLM 답변을 확인했다
- [ ] `/health/ready` 가 성공한다
- [ ] 오류가 나면 코드보다 먼저 환경 파일 존재 여부 → 파일 경로 → `working-directory` → 서버 배포 폴더를 확인할 수 있다
