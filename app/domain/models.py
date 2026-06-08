from dataclasses import dataclass

from app.domain.enums import BottomPattern


@dataclass(frozen=True)
class MarketInput:
    date: str
    kospi_close: float
    kospi_change_pt: float
    kospi_change_pct: float
    kospi_drawdown_pct: float
    disparity_20: float
    disparity_60: float
    below_ma20_ratio: float
    vkospi: float
    ma50_support: bool
    ma60_support: bool
    bottom_pattern: BottomPattern
    wti: float
    dubai: float
    us_gdp_yoy: float
    us_jobs: str
    kosdaq_close: float | None = None
    kosdaq_drawdown_pct: float | None = None
    us_10y_yield: float | None = None
    us_10y_source: str = "manual"
    oil_20d_avg: float | None = None
    oil_5d_change_pct: float | None = None
    oil_data_source: str = "manual"
    vkospi_source: str = "manual"
