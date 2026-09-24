# EC2 배포 명령어 정리 (weather-mcp)

로컬(Windows PowerShell) → EC2(Ubuntu) 로 .env 파일을 전송하는 과정에서 실행한 명령어 요약입니다. (오류, 중복 명령어는 제외)

## 1. 변수 설정

```powershell
# 프로젝트 경로, pem 키 경로, 접속할 EC2 서버 주소를 변수로 지정
$project = "C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project"
$keyPath = "$project\agent2.pem"
$server = "ubuntu@15.164.164.245"
```

## 2. 로컬 파일 존재 확인

```powershell
# 전송할 .env 파일과 pem 키 파일이 실제로 존재하는지 확인
Test-Path "$project\.env"
Test-Path $keyPath
```

## 3. EC2 호스트 키 확인

```powershell
# known_hosts에 EC2 서버의 호스트 키가 등록되어 있는지 확인
ssh-keygen -F 15.164.164.245 -f "$env:USERPROFILE\.ssh\known_hosts"
```

## 4. EC2에 배포 디렉터리 생성

```powershell
# EC2 인스턴스에 .env 파일을 저장할 디렉터리 생성
ssh -i $keyPath $server "mkdir -p ~/weather-mcp-deployment"
```

## 5. .env 파일 전송

```powershell
# 로컬의 .env 파일을 EC2 인스턴스의 weather-mcp-deployment 디렉터리로 전송
scp -i $keyPath "$project\.env" "${server}:~/weather-mcp-deployment/.env"
```

## 6. 파일 권한 설정 및 확인

```powershell
# 전송된 .env 파일의 권한을 소유자만 읽기/쓰기 가능(600)하도록 변경하고 결과 확인
ssh -i $keyPath $server "chmod 600 ~/weather-mcp-deployment/.env && ls -l ~/weather-mcp-deployment/.env"
```

## 7. 로컬 Docker 환경 확인

```powershell
# 로컬(Windows)에 설치된 Docker 및 Docker Compose 버전/정보 확인
docker info
docker compose version
```

## 8. pem 키 파일 권한 설정

```powershell
# Windows 파일의 상속 권한을 제거하고, 현재 사용자에게만 읽기 권한을 부여 (SSH가 개인키 권한이 너무 열려있으면 거부하기 때문)
icacls $keyPath /inheritance:r
icacls $keyPath /grant:r "$($env:USERNAME):(R)"
```

## 9. EC2 접속

```powershell
# pem 키를 이용해 EC2 인스턴스에 SSH 접속
ssh -i $keyPath ubuntu@15.164.164.245
```

## 10. EC2에 Docker 설치 및 설정

```bash
# 패키지 목록 갱신 후 docker, docker-compose-v2, git, curl 설치
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git curl

# Docker 서비스를 부팅 시 자동 시작하도록 설정하고 즉시 실행
sudo systemctl enable --now docker

# ubuntu 사용자를 docker 그룹에 추가하여 sudo 없이 docker 명령 사용 가능하도록 설정
sudo usermod -aG docker ubuntu

# 그룹 변경 사항 적용을 위해 세션 종료 후 재접속
exit
```

## 11. 재접속 후 Docker 설치 확인

```bash
# EC2에 재접속 (docker 그룹 권한 반영을 위해)
ssh -i $keyPath ubuntu@15.164.164.245

# 설치된 Docker 및 Compose 버전/정보 확인
docker info
docker compose version

# 현재 실행 중/생성된 컨테이너 및 이미지 목록 확인 (설치 직후이므로 비어있음)
docker ps -a
docker images
```
