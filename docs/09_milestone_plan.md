# MVP 마일스톤 계획

## 1. 문서 목적
이 문서는 `08_execution_plan.md`의 MVP Task를 실제 구현 순서에 맞춰 짧은 마일스톤으로 재구성한 계획이다.

핵심 목표는 2주 안에 빠른 작동 버전을 만들 수 있게 범위를 좁히는 것이다.

## 2. 마일스톤 개요
- Milestone 1: 핵심 도메인과 설정 준비
- Milestone 2: 판정과 리포트 생성 완성
- Milestone 3: 텔레그램 연결과 수동 실행 완성
- Milestone 4: 테스트와 최소 운영 보강

## 3. 마일스톤 상세
### Milestone 1. 핵심 도메인과 설정 준비
- [ ] 포함 Task
  - `MVP-01`
  - `MVP-08`

- [ ] 완료 조건
  - 입력 모델이 확정된다.
  - 환경변수 및 실행 모드 구조가 정리된다.

- [ ] 선행 의존성
  - `06_data_schema.md`
  - `02_prd_check_bottom_bot.md`

### Milestone 2. 판정과 리포트 생성 완성
- [ ] 포함 Task
  - `MVP-02`
  - `MVP-03`
  - `MVP-04`
  - `MVP-05`
  - `MVP-06`
  - `MVP-07`

- [ ] 완료 조건
  - 입력 검증이 동작한다.
  - 규칙 기반 판정이 동작한다.
  - 판정 근거 구조가 정의된다.
  - 한국어 리포트가 필수 섹션을 포함한다.
  - 투자 자문형 문체가 차단된다.

- [ ] 선행 의존성
  - `Milestone 1`
  - `04_logic_spec.md`
  - `05_prompt_spec.md`

### Milestone 3. 텔레그램 연결과 수동 실행 완성
- [ ] 포함 Task
  - `MVP-09`
  - `MVP-10`
  - `MVP-11`
  - `MVP-12`
  - `MVP-13`

- [ ] 완료 조건
  - 단일 실행 흐름이 동작한다.
  - 텔레그램 전송이 연결된다.
  - 수동 입력으로 end-to-end 실행이 가능하다.
  - 최소 저장 또는 로그 전략이 정리된다.
  - 오류 처리와 운영 로그가 남는다.

- [ ] 선행 의존성
  - `Milestone 2`

### Milestone 4. 테스트와 최소 운영 보강
- [ ] 포함 Task
  - `MVP-14`
  - `MVP-15`

- [ ] 완료 조건
  - 핵심 판정 로직 단위 테스트가 있다.
  - `입력 -> 검증 -> 판정 -> 리포트` 통합 테스트가 통과한다.

- [ ] 선행 의존성
  - `Milestone 3`

## 4. 권장 일정
### Week 1
- [ ] `Milestone 1` 완료
- [ ] `Milestone 2` 완료

### Week 2
- [ ] `Milestone 3` 완료
- [ ] `Milestone 4` 완료

## 5. 게이트 조건
- [ ] Gate A
  - 완료 조건: `Milestone 2` 전에는 텔레그램 연결보다 판정 결과 구조를 먼저 확정한다.

- [ ] Gate B
  - 완료 조건: `Milestone 3`이 끝나기 전에는 MVP 완료로 보지 않는다.

- [ ] Gate C
  - 완료 조건: `Milestone 4`가 끝나기 전에는 안정화 완료로 보지 않는다.

## 6. 최종 완료 기준
- [ ] 2주 MVP 완료
  - 완료 조건: `Milestone 1`부터 `Milestone 4`까지 완료되어 텔레그램 봇이 수동 입력 기준으로 실제 동작한다.

## 7. 관련 문서
- 실행 계획: `08_execution_plan.md`
- 구조 원칙: `07_project_structure_principles.md`
