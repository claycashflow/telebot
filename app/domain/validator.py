from app.domain.enums import BottomPattern
from app.domain.models import MarketInput


REQUIRED_FIELDS = {
    "date",
    "kospi_close",
    "kosdaq_close",
    "kospi_change_pt",
    "kospi_change_pct",
    "kospi_drawdown_pct",
    "kosdaq_drawdown_pct",
    "disparity_20",
    "disparity_60",
    "below_ma20_ratio",
    "vkospi",
    "ma50_support",
    "ma60_support",
    "bottom_pattern",
    "wti",
    "dubai",
    "us_gdp_yoy",
    "us_jobs",
}


class ValidationError(ValueError):
    pass


def validate_market_input(payload: dict) -> MarketInput:
    missing = REQUIRED_FIELDS.difference(payload.keys())
    if missing:
        raise ValidationError(f"누락된 필드가 있다: {sorted(missing)}")

    if float(payload["kospi_drawdown_pct"]) > 0 or float(payload["kosdaq_drawdown_pct"]) > 0:
        raise ValidationError("하락률 값은 0 이하여야 한다.")

    below = float(payload["below_ma20_ratio"])
    if not (0 <= below <= 100):
        raise ValidationError("below_ma20_ratio 값은 0~100 사이여야 한다.")

    try:
        bottom_pattern = BottomPattern(payload["bottom_pattern"])
    except ValueError as exc:
        allowed = [p.value for p in BottomPattern]
        raise ValidationError(f"bottom_pattern 값이 올바르지 않다. 허용값: {allowed}") from exc

    return MarketInput(
        date=str(payload["date"]),
        kospi_close=float(payload["kospi_close"]),
        kosdaq_close=float(payload["kosdaq_close"]),
        kospi_change_pt=float(payload["kospi_change_pt"]),
        kospi_change_pct=float(payload["kospi_change_pct"]),
        kospi_drawdown_pct=float(payload["kospi_drawdown_pct"]),
        kosdaq_drawdown_pct=float(payload["kosdaq_drawdown_pct"]),
        disparity_20=float(payload["disparity_20"]),
        disparity_60=float(payload["disparity_60"]),
        below_ma20_ratio=float(payload["below_ma20_ratio"]),
        vkospi=float(payload["vkospi"]),
        ma50_support=bool(payload["ma50_support"]),
        ma60_support=bool(payload["ma60_support"]),
        bottom_pattern=bottom_pattern,
        wti=float(payload["wti"]),
        dubai=float(payload["dubai"]),
        us_gdp_yoy=float(payload["us_gdp_yoy"]),
        us_jobs=str(payload["us_jobs"]),
    )
