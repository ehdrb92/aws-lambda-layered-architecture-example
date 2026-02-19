# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python 3.13+ AWS Lambda 프로젝트. 레이어드 아키텍처 기반으로 구성되며 `uv`로 패키지를 관리한다.

## Commands

```bash
# 의존성 설치
uv sync

# 패키지 추가
uv add <package>

# 전체 테스트 실행
uv run python -m pytest tests/

# 특정 파일만 실행
uv run python -m pytest tests/service/test_todo_service.py

# 특정 테스트만 실행
uv run python -m pytest tests/service/test_todo_service.py::TestCreateTodo::test_returns_repository_save_result
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
