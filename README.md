# 시장 저점 판독 텔레그램 봇

한국 주식시장(KOSPI/KOSDAQ) 장 마감 데이터를 바탕으로 시장 저점 상태를 규칙 기반으로 판독하고, 한국어 리포트를 텔레그램으로 전송하는 MVP 프로젝트다.

## 현재 범위
- 수동 입력 기반 실행
- 입력 검증
- 규칙 기반 저점 판정
- 한국어 리포트 생성
- 텔레그램 명령 처리
- 텔레그램 메시지 전송

## 현재 확인된 상태
- `ai` conda 환경에서 의존성 설치 완료
- `python -m pytest -q` 기준 테스트 2건 통과
- 샘플 리포트의 텔레그램 전송 성공 확인
- 회사 환경 특성상 polling 모드 또는 외부 네트워크 호출은 제약이 있을 수 있음

## 문서
- [도메인 정의](D:\_20. source\telebot\docs\01_domain.md)
- [PRD](D:\_20. source\telebot\docs\02_prd_check_bottom_bot.md)
- [판정 로직](D:\_20. source\telebot\docs\04_logic_spec.md)
- [프롬프트 명세](D:\_20. source\telebot\docs\05_prompt_spec.md)
- [데이터 스키마](D:\_20. source\telebot\docs\06_data_schema.md)
- [MVP 실행 계획](D:\_20. source\telebot\docs\08_execution_plan.md)
- [MVP 마일스톤 계획](D:\_20. source\telebot\docs\09_milestone_plan.md)
- [텔레그램 봇 생성 및 배포 절차](D:\_20. source\telebot\docs\11_telegram_bot_setup_and_deploy.md)

## 빠른 시작
### 1. 권장 실행 환경
현재 기준 권장 환경은 conda의 `ai` 환경이다.

```powershell
conda run -n ai python --version
```

### 2. 의존성 설치
```powershell
conda run -n ai python -m pip install -r requirements.txt
```

### 3. `.env` 설정
`.env.example`를 참고해서 프로젝트 루트에 `.env` 파일을 만든다.

```env
APP_ENV=local
TELEGRAM_BOT_TOKEN=발급받은_토큰
TELEGRAM_CHAT_ID=채팅_ID
```

### 4. 실행
```powershell
conda run -n ai python main.py
```

`conda run`이 회사 환경에서 불안정하면 아래처럼 환경의 Python 경로를 직접 호출하는 방식이 더 안정적일 수 있다.

```powershell
D:\miniconda3\envs\ai\python.exe main.py
```

## 텔레그램 명령
### `/start`
- 봇 소개와 `/check` 사용법을 보여준다.

### `/check`
- JSON 입력을 받아 시장 상태를 판정한다.
- 가장 쉬운 방식은 봇에게 JSON 메시지를 보내고, 그 메시지에 답장(reply)한 상태에서 `/check`를 보내는 것이다.
- 또는 `/check { ... }` 형태로 한 줄 JSON을 붙여도 된다.

예시 JSON:

```json
{
  "date": "2026-03-23",
  "kospi_close": 2612.34,
  "kosdaq_close": 845.22,
  "kospi_drawdown_pct": -19.2,
  "kosdaq_drawdown_pct": -22.1,
  "disparity_20": 91.3,
  "disparity_60": 93.0,
  "vkospi": 47.0,
  "ma50_support": true,
  "ma60_support": false,
  "bottom_pattern": "W_second_bottom",
  "wti": 84.2,
  "dubai": 81.7,
  "us_gdp_yoy": 3.2,
  "us_jobs": "stable",
  "semiconductor_earnings_view": "positive"
}
```

## 프로젝트 구조
```text
app/
  application/
  bot/
  config/
  domain/
tests/
docs/
main.py
```

## 테스트
```powershell
conda run -n ai python -m pytest -q
```

`conda run`이 불안정하면 아래처럼 직접 실행할 수 있다.

```powershell
D:\miniconda3\envs\ai\python.exe -m pytest -q
```

## 주의사항
- 이 프로젝트 결과는 투자 판단 보조용이다.
- 투자 자문처럼 단정적으로 사용하면 안 된다.
- 문서 기준으로 로직과 출력 형식을 유지해야 한다.
- 회사 네트워크 정책 때문에 텔레그램 polling 또는 외부 API 호출이 제한될 수 있다.
