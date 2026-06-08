# 입력 데이터 스키마

```json
{
  "date": "2026-03-23",
  "kospi_close": 2612.34,
  "kospi_change_pt": -23.5,
  "kospi_change_pct": -0.89,
  "kospi_drawdown_pct": -19.2,
  "disparity_20": 91.3,
  "disparity_60": 93.0,
  "below_ma20_ratio": 68.4,
  "vkospi": 47.0,
  "ma50_support": true,
  "ma60_support": false,
  "bottom_pattern": "W_second_bottom",
  "wti": 84.2,
  "dubai": 81.7,
  "oil_20d_avg": 86.4,
  "oil_5d_change_pct": 2.1,
  "oil_data_source": "manual",
  "us_gdp_yoy": 3.2,
  "us_jobs": "stable",
  "us_10y_yield": 4.2,
  "us_10y_source": "manual",
  "vkospi_source": "manual"
}
```

## 필드 설명
- `kospi_change_pt`: KOSPI 전일 대비 등락폭 (포인트, 하락 시 음수)
- `kospi_change_pct`: KOSPI 전일 대비 등락률 (%, 하락 시 음수)
- `kospi_drawdown_pct`: 52주 고점 대비 하락률, 음수 값
- `disparity_20` / `disparity_60`: 이격도 (100 기준)
- `below_ma20_ratio`: 전종목 중 20일 MA 하회 비율 (0~100)
- `vkospi`: 변동성 지표
- `ma50_support` / `ma60_support`: 이동평균선 지지 여부
- `bottom_pattern`: `V_attempt`, `W_forming`, `W_second_bottom`, `Panic_capitulation`
- `wti`: WTI 원유 가격
- `dubai`: Dubai 원유 가격. 자동 수집에서 실제 Dubai 데이터 확보가 불가능한 경우 대체 지표 사용 여부를 `oil_data_source`에 명시한다.
- `oil_20d_avg`: 선택 필드. WTI/Dubai 중 더 높은 유가 기준의 20거래일 평균. 90 이상이면 고유가 고착 부담으로 본다.
- `oil_5d_change_pct`: 선택 필드. WTI/Dubai 중 더 높은 유가 기준의 최근 5거래일 변화율. 8% 이상이면 단기 급등 위험으로 본다.
- `oil_data_source`: 선택 필드. 유가 데이터 출처 또는 대체 지표 사용 여부
- `us_gdp_yoy`: 미국 실질 GDP 전년 대비 증가율
- `us_jobs`: 미국 고용 동향 (`strong`, `stable`, `weak` 등)
- `us_10y_yield`: 선택 필드. 미국 10년물 국채 금리(%). 4.5 이상이면 금리 부담, 5.0 이상이면 강한 금리 부담으로 본다.
- `us_10y_source`: 선택 필드. 미국 10년물 금리 데이터 출처
- `vkospi_source`: 선택 필드. 실제 VKOSPI인지, 자동 수집의 역사적 변동성 근사값인지 표시
- `kosdaq_close` / `kosdaq_drawdown_pct`: 선택 호환 필드. 현재 판정 로직에는 사용하지 않는다.
