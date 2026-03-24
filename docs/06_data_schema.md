# 입력 데이터 스키마

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

## 필드 설명
- `kospi_drawdown_pct`: 최근 고점 대비 하락률, 음수 값
- `disparity_20` / `disparity_60`: 이격도
- `vkospi`: 변동성 지표
- `ma50_support` / `ma60_support`: 이동평균선 지지 여부
- `bottom_pattern`: `V_attempt`, `W_forming`, `W_second_bottom`, `Panic_capitulation`
- `semiconductor_earnings_view`: `positive`, `neutral`, `negative`
