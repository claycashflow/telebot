from app.domain.judgement import evaluate_market
from app.domain.models import MarketInput
from app.domain.enums import BottomPattern


def build_input(**overrides):
    payload = {
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
        "ma50_support": True,
        "ma60_support": False,
        "bottom_pattern": BottomPattern.W_SECOND_BOTTOM,
        "wti": 84.2,
        "dubai": 81.7,
        "us_gdp_yoy": 3.2,
        "us_jobs": "stable",
    }
    payload.update(overrides)
    return MarketInput(**payload)


def test_evaluate_market_returns_valid_status():
    result = evaluate_market(build_input())
    assert result["status"] in {"추가 조정 필요", "저점 근접", "진 바닥 확인"}
    assert isinstance(result["score"], int)
    assert result["reasons"]
