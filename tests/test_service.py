from app.application.service import run_market_check


def test_run_market_check_generates_report():
    payload = {
        "date": "2026-03-23",
        "kospi_close": 2612.34,
        "kospi_change_pt": -23.5,
        "kospi_change_pct": -0.89,
        "kospi_drawdown_pct": -19.2,
        "disparity_20": 91.3,
        "disparity_60": 93.0,
        "below_ma20_ratio": 68.4,
        "vkospi": 47.0,
        "ma50_support": True,
        "ma60_support": False,
        "bottom_pattern": "W_second_bottom",
        "wti": 84.2,
        "dubai": 81.7,
        "oil_20d_avg": 86.4,
        "oil_5d_change_pct": 2.1,
        "us_gdp_yoy": 3.2,
        "us_jobs": "stable",
        "us_10y_yield": 4.2,
    }
    _, judgement, report = run_market_check(payload)
    assert judgement["status"]
    assert "저점 판독 결과" in report
    assert "KOSDAQ 하락률" not in report
    assert "유가 20일 평균" in report
    assert "미국 10년물 금리" in report
