# run-bot

텔레그램 봇을 실제로 실행하거나 샘플 모드로 검증할 때 사용한다.

## 준비
- `.env`에 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`가 설정되어 있어야 한다.
- 회사 환경에서 polling이 막힐 수 있으므로, 먼저 단건 전송이나 샘플 실행부터 확인한다.

## 실행 명령
```powershell
D:\miniconda3\envs\ai\python.exe main.py
```

## 기대 동작
- 토큰이 없으면 샘플 리포트를 콘솔에 출력한다.
- 토큰이 있으면 텔레그램 polling 모드로 진입한다.
- 네트워크 제약이 있으면 polling 대신 단건 전송 확인으로 대체한다.

## 점검 포인트
- `.env` 로딩이 되는가
- 텔레그램 전송 또는 polling 기동이 되는가
- 회사 네트워크 정책 때문에 외부 API가 막히는지 확인했는가
