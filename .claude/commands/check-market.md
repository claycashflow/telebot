# check-market

현재 구현된 시장 저점 판독 흐름을 점검할 때 사용한다.

## 절차
1. `docs/04_logic_spec.md`, `docs/05_prompt_spec.md`, `docs/06_data_schema.md`를 확인한다.
2. `app/domain`, `app/application`, `app/bot`의 관련 코드를 읽는다.
3. 아래 명령으로 테스트를 실행한다.

```powershell
D:\miniconda3\envs\ai\python.exe -m pytest -q
```

4. 필요하면 샘플 실행으로 리포트를 확인한다.

```powershell
D:\miniconda3\envs\ai\python.exe main.py
```

## 체크 포인트
- 입력 검증이 문서 스키마와 일치하는가
- 판정 상태가 3종으로 제한되는가
- 리포트 섹션 순서가 문서와 일치하는가
- 텔레그램 연동 코드가 도메인 로직과 분리되어 있는가
