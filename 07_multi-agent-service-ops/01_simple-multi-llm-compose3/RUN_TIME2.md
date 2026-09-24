# Docker Compose 종료 및 이미지 삭제 방법 비교

두 방식의 핵심 차이는 **삭제 범위**입니다.

## 1. 지정한 이미지 직접 삭제

```bash
docker compose -f compose.release.yml down

docker image rm \
  young0707/simple-app-backend:1.0.0 \
  young0707/simple-app-frontend:1.0.0
```

- 현재 Compose의 컨테이너와 네트워크를 제거합니다.
- 지정한 Backend와 Frontend 이미지 2개만 정확히 삭제합니다.
- 삭제 대상을 명확하게 통제할 수 있습니다.

## 2. `--rmi local` 사용

```bash
docker compose -f compose.release.yml down --remove-orphans --rmi local
```

- 현재 Compose의 컨테이너와 네트워크를 제거합니다.
- `--remove-orphans`는 Compose 파일에 더 이상 정의되지 않은 같은 프로젝트의 컨테이너도 제거합니다.
- `--rmi local`은 Compose 서비스가 사용하는 이미지 중 **사용자 지정 태그가 없는 로컬 이미지**만 제거합니다.
- 볼륨은 삭제하지 않습니다.

현재 이미지에는 사용자 지정 태그가 있습니다.

```text
young0707/simple-app-backend:1.0.0
young0707/simple-app-frontend:1.0.0
```

따라서 `--rmi local`로는 이 두 이미지가 삭제되지 않을 가능성이 큽니다. Docker 공식 문서에서도 `local`은 사용자 지정 태그가 없는 이미지만 제거한다고 설명합니다.

참고: [Docker Compose down 공식 문서](https://docs.docker.com/reference/cli/docker/compose/down/)

## Compose에서 사용하는 이미지 모두 삭제

두 이미지를 Compose와 함께 확실히 삭제하려면 다음 명령을 사용할 수 있습니다.

```bash
docker compose -f compose.release.yml down --remove-orphans --rmi all
```

이 명령은 Compose가 사용하는 Backend와 Frontend 이미지를 모두 삭제합니다. Redis와 PostgreSQL이 이 Compose 파일 밖에서 별도로 실행 중이라면 영향을 받지 않습니다.

## 권장 방법

정확히 두 이미지만 삭제하려면 다음 방법이 가장 안전합니다.

```bash
docker compose -f compose.release.yml down --remove-orphans

docker image rm \
  young0707/simple-app-backend:1.0.0 \
  young0707/simple-app-frontend:1.0.0
```

> 어느 방법도 `-v` 옵션을 붙이지 않는 한 Docker 볼륨을 삭제하지 않습니다.
