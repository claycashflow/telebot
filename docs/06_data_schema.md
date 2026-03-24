# 입력 데이터 스키마

```json
{
  "date": "2026-03-23",
  "kospi_close": 2612.34,
  "kosdaq_close": 845.22,
  "kospi_change_pt": -23.5,
  "kospi_change_pct": -0.89,
  "kospi_drawdown_pct": -19.2,
  "kosdaq_drawdown_pct": -22.1,
  "disparity_20": 91.3,
  "disparity_60": 93.0,
  "below_ma20_ratio": 68.4,
  "vkospi": 47.0,
  "ma50_support": true,
  "ma60_support": false,
  "bottom_pattern": "W_second_bottom",
  "wti": 84.2,
  "dubai": 81.7,
  "us_gdp_yoy": 3.2,
  "us_jobs": "stable"
}
```

## 필드 설명
- `kospi_change_pt`: KOSPI 전일 대비 등락폭 (포인트, 하락 시 음수)
- `kospi_change_pct`: KOSPI 전일 대비 등락률 (%, 하락 시 음수)
- `kospi_drawdown_pct`: 52주 고점 대비 하락률, 음수 값
- `kosdaq_drawdown_pct`: 52주 고점 대비 하락률, 음수 값
- `disparity_20` / `disparity_60`: 이격도 (100 기준)
- `below_ma20_ratio`: 전종목 중 20일 MA 하회 비율 (0~100)
- `vkospi`: 변동성 지표
- `ma50_support` / `ma60_support`: 이동평균선 지지 여부
- `bottom_pattern`: `V_attempt`, `W_forming`, `W_second_bottom`, `Panic_capitulation`
