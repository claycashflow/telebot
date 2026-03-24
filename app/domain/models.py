from dataclasses import dataclass

from app.domain.enums import BottomPattern


@dataclass(frozen=True)
class MarketInput:
    date: str
    kospi_close: float
    kosdaq_close: float
    kospi_change_pt: float
    kospi_change_pct: float
    kospi_drawdown_pct: float
    kosdaq_drawdown_pct: float
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
