from app.domain.enums import BottomPattern, EarningsView
from app.domain.models import MarketInput


REQUIRED_FIELDS = {
    "date",
    "kospi_close",
    "kosdaq_close",
    "kospi_drawdown_pct",
    "kosdaq_drawdown_pct",
    "disparity_20",
    "disparity_60",
    "vkospi",
    "ma50_support",
    "ma60_support",
    "bottom_pattern",
    "wti",
    "dubai",
    "us_gdp_yoy",
    "us_jobs",
    "semiconductor_earnings_view",
}


class ValidationError(ValueError):
    pass


def validate_market_input(payload: dict) -> MarketInput:
    missing = REQUIRED_FIELDS.difference(payload.keys())
    if missing:
        raise ValidationError(f"Missing required fields: {sorted(missing)}")

    if float(payload["kospi_drawdown_pct"]) > 0 or float(payload["kosdaq_drawdown_pct"]) > 0:
        raise ValidationError("Drawdown values must be zero or negative.")

    try:
        bottom_pattern = BottomPattern(payload["bottom_pattern"])
    except ValueError as exc:
        raise ValidationError("Invalid bottom_pattern.") from exc

    try:
        earnings_view = EarningsView(payload["semiconductor_earnings_view"])
    except ValueError as exc:
        raise ValidationError("Invalid semiconductor_earnings_view.") from exc

    return MarketInput(
        date=str(payload["date"]),
        kospi_close=float(payload["kospi_close"]),
        kosdaq_close=float(payload["kosdaq_close"]),
        kospi_drawdown_pct=float(payload["kospi_drawdown_pct"]),
        kosdaq_drawdown_pct=float(payload["kosdaq_drawdown_pct"]),
        disparity_20=float(payload["disparity_20"]),
        disparity_60=float(payload["disparity_60"]),
        vkospi=float(payload["vkospi"]),
        ma50_support=bool(payload["ma50_support"]),
        ma60_support=bool(payload["ma60_support"]),
        bottom_pattern=bottom_pattern,
        wti=float(payload["wti"]),
        dubai=float(payload["dubai"]),
        us_gdp_yoy=float(payload["us_gdp_yoy"]),
        us_jobs=str(payload["us_jobs"]),
        semiconductor_earnings_view=earnings_view,
    )
