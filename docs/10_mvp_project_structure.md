# MVP 프로젝트 구조

## 1. 문서 목적
이 문서는 빠른 MVP 개발을 위한 실제 디렉토리 구조와 파일 책임을 정의한다.

초기 구현은 `단일 Python 텔레그램 봇 앱`으로 두고, 웹 프론트엔드와 별도 백엔드 서버는 두지 않는다.

## 2. 구조 원칙
- 하나의 프로세스에서 `입력 -> 검증 -> 판정 -> 리포트 -> 전송`을 처리한다.
- 도메인 로직은 텔레그램 전송 코드와 분리한다.
- 외부 연동은 얇게 두고, 핵심 로직은 테스트 가능한 순수 함수에 가깝게 유지한다.
- 저장소가 필요하면 초기에는 DB 대신 파일 또는 로그 기반으로 시작한다.

## 3. 권장 디렉토리
```text
telebot/
  .claude/
    CLAUDE.md
    commands/
      check-market.md
      run-bot.md
  app/
    application/
      service.py
    bot/
      handlers.py
      telegram_sender.py
    config/
      settings.py
    domain/
      enums.py
      models.py
      validator.py
      judgement.py
      report.py
  tests/
    test_judgement.py
    test_service.py
  .env.example
  main.py
  requirements.txt
```

## 4. 디렉토리별 책임
### `app/domain`
- 입력 모델
- enum 및 상태값
- 입력 검증
- 저점 판정 규칙
- 리포트 생성

### `app/application`
- 도메인 로직을 조합하는 실행 흐름
- 단일 유스케이스 진입점

### `app/bot`
- 텔레그램 메시지 송신
- 텔레그램 명령 또는 수동 테스트용 핸들러

### `app/config`
- 환경변수 로딩
- 실행 모드 및 설정 관리

### `tests`
- 판정 규칙 단위 테스트
- 서비스 흐름 통합 테스트

## 5. MVP에서 두지 않는 것
- `frontend/`
- `backend/`
- `api/`
- `database/`
- `migrations/`

이 항목들은 운영 확장 단계에서 필요할 때만 추가한다.

단, Claude Code 호환을 위해 `.claude/` 디렉토리는 둔다.

## 6. 초기 실행 흐름
- `main.py`가 설정을 로드한다.
- 입력 데이터 예시 또는 명령을 받아 `application/service.py`를 호출한다.
- 서비스는 검증, 판정, 리포트 생성을 수행한다.
- 최종 결과를 `bot/telegram_sender.py`를 통해 전송한다.

## 7. 완료 기준
- 디렉토리 구조가 실제 코드와 일치한다.
- 각 파일 책임이 중복되지 않는다.
- `domain`은 텔레그램 라이브러리에 의존하지 않는다.
- `main.py` 하나로 수동 실행이 가능하다.
