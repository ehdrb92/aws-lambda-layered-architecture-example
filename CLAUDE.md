# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python 3.13+ AWS Lambda 프로젝트. 레이어드 아키텍처 기반으로 구성되며 `uv`로 패키지를 관리한다.
인프라는 AWS SAM(`template.yaml`)으로 정의하고, GitHub Actions로 CI/CD를 자동화한다.

## Commands

```bash
# 의존성 설치 (dev 포함)
uv sync

# 패키지 추가 (런타임)
uv add <package>

# 패키지 추가 (dev 전용)
uv add --dev <package>

# 전체 테스트 실행
uv run python -m pytest tests/

# 특정 파일만 실행
uv run python -m pytest tests/service/test_todo_service.py

# 특정 테스트만 실행
uv run python -m pytest tests/service/test_todo_service.py::TestCreateTodo::test_returns_repository_save_result

# SAM 로컬 빌드
sam build

# SAM 배포 (수동)
sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --resolve-s3 --stack-name layered-architecture-example --capabilities CAPABILITY_IAM --region ap-northeast-2
```

## Architecture

### 레이어 구조 및 호출 방향

```
lambda_function.py  →  container.py  →  presentation  →  service  →  repository
(라우팅)               (DI 조립)         (Controller)    (비즈니스)    (저장소)
```

### 레이어별 규칙

- **`lambda_function.py`**: HTTP method/path 기반 라우팅만 담당. 비즈니스 로직과 DI 조립을 포함하지 않는다.
- **`container.py`**: 구체 클래스를 생성하고 의존성을 조립하는 유일한 지점. `Container` 클래스에 `@cached_property`로 각 인스턴스를 선언하며, 모듈 하단의 `container = Container()`가 Lambda 콜드 스타트 시 한 번 초기화된다.
- **`presentation/`**: Controller 클래스만 위치. Lambda event에서 파라미터를 추출하고 응답을 포맷한다. Service 인터페이스에만 의존한다.
- **`service/`**: 비즈니스 로직. 인터페이스 없이 구현체만 작성하며, 생성자에서 `repository/interfaces/`의 ABC를 주입받는다.
- **`repository/interfaces/`**: ABC로 저장소 계약을 정의한다. 구현체가 어떤 저장소를 쓰는지 알지 못한다.
- **`repository/`**: 구현체 파일명에 저장소 이름을 prefix로 명시한다 (예: `dynamodb_user_repository.py`).

### 새 도메인 추가 시 작성 순서

1. `repository/interfaces/` — ABC 정의
2. `repository/` — 구현체 작성
3. `service/` — Service 클래스 작성 (repository ABC 주입)
4. `presentation/` — Controller 클래스 작성 (service 주입)
5. `container.py` — `@cached_property` 3개 추가 (repository, service, controller)
6. `lambda_function.py` — 라우팅 규칙 추가
7. `template.yaml` 수정 불필요 — `/{proxy+}` catch-all이 모든 경로를 Lambda로 전달함

## Infra (AWS SAM)

### 구조

```
template.yaml  →  CloudFormation 스택 (layered-architecture-example)
                    ├─ Lambda 함수 (layered-architecture-example)
                    └─ API Gateway (/{proxy+} → Lambda Proxy Integration)
```

### 주요 파일

- **`template.yaml`**: Lambda + API Gateway 인프라 정의. 런타임, 핸들러, 라우팅 설정 포함.
- **`pyproject.toml`**: `[project].dependencies`는 런타임 의존성만. `[dependency-groups].dev`에 테스트 도구(pytest 등)를 관리. SAM build 시 dev 의존성은 Lambda 패키지에 포함되지 않는다.

### API Gateway 라우팅 방식

API Gateway는 `/{proxy+}` catch-all로 모든 요청을 Lambda 하나로 전달한다.
라우팅 로직은 `lambda_function.py` 내부에서 처리하므로, 새 엔드포인트 추가 시 `template.yaml`은 변경하지 않는다.

## CI/CD (GitHub Actions)

### 파일 위치

`.github/workflows/deploy.yml`

### 흐름

```
main 브랜치 push
  └─ test job:    uv sync → pytest
  └─ deploy job:  (test 통과 시) sam build → sam deploy
```

### 필요한 GitHub Secrets

| Secret | 설명 |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM 사용자 Access Key |
| `AWS_SECRET_ACCESS_KEY` | IAM 사용자 Secret Key |

### IAM 권한 (GitHub Actions용 IAM 사용자)

SAM 배포에 필요한 AWS 관리형 정책:
- `AWSCloudFormationFullAccess`
- `AmazonS3FullAccess`
- `AWSLambda_FullAccess`
- `AmazonAPIGatewayAdministrator`
- `IAMFullAccess`
