# CLAUDE.md

## 목적
- 이 저장소는 한국 주식시장(KOSPI/KOSDAQ) 장 마감 데이터를 바탕으로 시장 저점 여부를 판독하는 텔레그램 봇 프로젝트다.
- 현재 기준 구현 목표는 `단일 Python 텔레그램 봇 MVP`다.
- 핵심 흐름은 `입력 -> 검증 -> 판정 -> 리포트 생성 -> 텔레그램 전송`이다.

## 우선 참조 문서
- 작업 전 아래 문서를 우선 읽고 따른다.
- `docs/01_domain.md`
- `docs/02_prd_check_bottom_bot.md`
- `docs/03_user_scenario.md`
- `docs/04_logic_spec.md`
- `docs/05_prompt_spec.md`
- `docs/06_data_schema.md`
- `docs/07_project_structure_principles.md`
- `docs/08_execution_plan.md`
- `docs/09_milestone_plan.md`
- `docs/10_mvp_project_structure.md`
- `docs/11_telegram_bot_setup_and_deploy.md`

## 작업 원칙
- 규칙 기반 판정 결과를 최우선으로 사용한다.
- 문서에 정의된 도메인 용어와 입력 필드 이름을 임의로 바꾸지 않는다.
- 현재 MVP는 웹 프론트엔드와 별도 백엔드 서버를 두지 않는다.
- Python 단일 애플리케이션 구조를 유지한다.
- 자동 데이터 수집은 확장 범위이며, 현재는 수동 입력 경로가 우선이다.
- 불확실한 내용은 추정으로 채우지 말고 문서와 코드 기준으로 확인한다.

## 도메인 규칙
- 최종 판정 상태는 아래 3개만 허용한다.
- `추가 조정 필요`
- `저점 근접`
- `진 바닥 확인`
- `bottom_pattern` 허용값은 `V_attempt`, `W_forming`, `W_second_bottom`, `Panic_capitulation`이다.
- `semiconductor_earnings_view` 허용값은 `positive`, `neutral`, `negative`다.
- 하락률 값은 최근 고점 대비 하락률이며 음수 값 전제를 유지한다.

## 출력 원칙
- 사용자 대상 출력은 기본적으로 한국어로 작성한다.
- 리포트는 가능하면 아래 순서를 유지한다.
- `현 시점 저점 판독 결과`
- `판단 근거 (데이터 분석)`
- `매크로 상황 분석`
- `최종 투자 의견`
- `주목할 업종`
- 과도한 확신 표현, 투자 자문형 단정, 근거 없는 업종 추천을 피한다.

## 구현 원칙
- 도메인 로직은 `app/domain`에 둔다.
- 실행 흐름 조합은 `app/application`에 둔다.
- 텔레그램 연동은 `app/bot`에 둔다.
- 설정 로딩은 `app/config`에 둔다.
- 핵심 로직은 테스트 가능한 순수 함수에 가깝게 유지한다.
- 텔레그램 연동 코드가 도메인 로직을 침범하면 안 된다.

## 실행 환경
- 권장 Python 환경은 conda의 `ai` 환경이다.
- 의존성 설치 예시:
- `conda run -n ai python -m pip install -r requirements.txt`
- 실행 예시:
- `conda run -n ai python main.py`
- 회사 환경에서 `conda run`이 불안정하면 아래 경로를 직접 사용할 수 있다.
- `D:\miniconda3\envs\ai\python.exe main.py`

## 테스트 원칙
- 테스트는 `tests/` 아래에 둔다.
- 핵심 우선순위는 `입력 검증 -> 판정 로직 -> 리포트 생성 -> 서비스 흐름`이다.
- 같은 입력에 대해 같은 결과가 나오는지를 항상 확인한다.

## Git 작업 원칙
- `.env`와 비밀값은 커밋하지 않는다.
- 의미 없는 대규모 리네이밍을 피한다.
- 문서 변경과 코드 변경이 함께 가면, 가능한 한 문서 정합성을 먼저 맞춘다.

## Claude에서 자주 할 작업
- 구현 전: 관련 `docs/` 문서 확인
- 코드 변경 후: `D:\miniconda3\envs\ai\python.exe -m pytest -q`
- 수동 실행 확인: `D:\miniconda3\envs\ai\python.exe main.py`
