from app.domain.judgement import evaluate_market
from app.domain.models import MarketInput
from app.domain.enums import BottomPattern


def build_input(**overrides):
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
        "bottom_pattern": BottomPattern.W_SECOND_BOTTOM,
        "wti": 84.2,
        "dubai": 81.7,
        "us_gdp_yoy": 3.2,
        "us_jobs": "stable",
        "us_10y_yield": 4.2,
    }
    payload.update(overrides)
    return MarketInput(**payload)


def test_evaluate_market_returns_valid_status():
    result = evaluate_market(build_input())
    assert result["status"] in {"추가 조정 필요", "저점 근접", "진 바닥 확인"}
    assert isinstance(result["score"], int)
    assert result["reasons"]


def test_sample_score_reflects_high_oil_penalty():
    result = evaluate_market(build_input())
    assert result["score"] == 8
    assert result["status"] == "진 바닥 확인"


def test_sustained_high_oil_adds_penalty():
    result = evaluate_market(build_input(oil_20d_avg=92.0))
    assert result["score"] == 7
    assert "20일 평균 유가가 90달러 이상으로 고유가 고착 부담이 있다." in result["reasons"]


def test_short_term_oil_spike_adds_penalty():
    result = evaluate_market(build_input(oil_5d_change_pct=8.0))
    assert result["score"] == 7
    assert "최근 5거래일 유가 급등으로 물가·금리 부담이 재부각될 수 있다." in result["reasons"]


def test_kosdaq_drawdown_is_not_used_for_judgement():
    result = evaluate_market(
        build_input(
            kospi_drawdown_pct=-16.2,
            kosdaq_drawdown_pct=-24.0,
            disparity_20=94.3,
            disparity_60=96.0,
            vkospi=62.5,
            wti=94.5,
            dubai=97.6,
        )
    )
    assert "하락률이 깊어 침체 가능성도 함께 점검해야 한다." not in result["reasons"]


def test_us_10y_yield_adds_penalty():
    result = evaluate_market(build_input(us_10y_yield=4.5))
    assert result["score"] == 7
    assert "미국 10년물 금리가 4.5% 이상으로 밸류에이션 부담이 있다." in result["reasons"]


def test_us_10y_yield_above_five_adds_extra_penalty():
    result = evaluate_market(build_input(us_10y_yield=5.0))
    assert result["score"] == 6
    assert "미국 10년물 금리가 5% 이상으로 금리 부담이 강하다." in result["reasons"]
