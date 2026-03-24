"""
장 마감 데이터 자동 수집 모듈.

백엔드 구성:
- yfinance         : KOSPI(^KS11), KOSDAQ(^KQ11), WTI(CL=F), 브렌트유(BZ=F)
- FinanceDataReader: KOSPI 시총 상위 50종목 개별 시세 → below_ma20_ratio 계산
- fredapi          : 미국 GDP YoY, 고용 동향 (FRED_API_KEY 설정 시)

KRX 자체 API(pykrx, fdr KS11 등)는 세션 인증 이슈로 사용하지 않는다.
"""

import datetime
import random

import numpy as np
import pandas as pd
import yfinance as yf

# KOSPI 시총 상위 50 종목 코드 (FinanceDataReader 형식 — 6자리)
_KOSPI_TOP50 = [
    "005930", "000660", "005380", "000270", "051910",
    "006400", "035420", "035720", "096770", "017670",
    "030200", "032830", "086790", "105560", "055550",
    "316140", "003490", "010950", "009540", "028260",
    "012330", "009830", "011170", "010130", "011200",
    "034220", "042660", "018260", "066570", "004020",
    "003550", "000810", "329180", "015760", "001570",
    "000720", "034730", "011790", "023530", "097950",
    "033780", "000100", "002790", "021240", "008770",
    "036460", "006280", "000780", "009150", "004170",
]


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

def collect_market_data(fred_api_key: str = "") -> dict:
    """장 마감 데이터를 수집해 validator 호환 dict 로 반환한다."""
    today = _last_trading_date()
    start = today - datetime.timedelta(days=300)

    kospi_hist  = _fetch_yf("^KS11", start, today)
    kosdaq_hist = _fetch_yf("^KQ11", start, today)

    if kospi_hist.empty or kosdaq_hist.empty:
        raise RuntimeError("KOSPI/KOSDAQ 데이터를 가져오지 못했다. 네트워크를 확인해주세요.")

    kospi_cl  = kospi_hist["Close"].squeeze()
    kosdaq_cl = kosdaq_hist["Close"].squeeze()

    kospi_close  = round(float(kospi_cl.iloc[-1]), 2)
    kospi_prev   = round(float(kospi_cl.iloc[-2]), 2)
    kosdaq_close = round(float(kosdaq_cl.iloc[-1]), 2)

    kospi_change_pt  = round(kospi_close - kospi_prev, 2)
    kospi_change_pct = round(kospi_change_pt / kospi_prev * 100, 2)

    # 52주 고점 대비 하락률
    kospi_52w_high  = float(kospi_hist["High"].squeeze().tail(252).max())
    kosdaq_52w_high = float(kosdaq_hist["High"].squeeze().tail(252).max())
    kospi_drawdown_pct  = round((kospi_close  - kospi_52w_high)  / kospi_52w_high  * 100, 1)
    kosdaq_drawdown_pct = round((kosdaq_close - kosdaq_52w_high) / kosdaq_52w_high * 100, 1)

    # 이격도 (20일, 60일)
    ma20 = float(kospi_cl.tail(20).mean())
    ma50 = float(kospi_cl.tail(50).mean())
    ma60 = float(kospi_cl.tail(60).mean())
    disparity_20 = round(kospi_close / ma20 * 100, 1)
    disparity_60 = round(kospi_close / ma60 * 100, 1)

    # 이동평균 지지 (±1% 이내)
    ma50_support = bool(kospi_close >= ma50 * 0.99)
    ma60_support = bool(kospi_close >= ma60 * 0.99)

    # V-KOSPI: 20일 역사적 변동성으로 근사
    vkospi = _calc_vkospi(kospi_cl)

    # 전종목 20일 MA 하회 비율
    below_ma20_ratio = _get_below_ma20_ratio(today)

    # 바닥 패턴
    bottom_pattern = _detect_bottom_pattern(kospi_cl.values)

    # 유가
    wti   = _get_yf_price("CL=F")
    dubai = _get_yf_price("BZ=F")

    # 미국 매크로
    us_gdp_yoy, us_jobs = _get_us_macro(fred_api_key)

    return {
        "date": today.strftime("%Y-%m-%d"),
        "kospi_close": kospi_close,
        "kosdaq_close": kosdaq_close,
        "kospi_change_pt": kospi_change_pt,
        "kospi_change_pct": kospi_change_pct,
        "kospi_drawdown_pct": kospi_drawdown_pct,
        "kosdaq_drawdown_pct": kosdaq_drawdown_pct,
        "disparity_20": disparity_20,
        "disparity_60": disparity_60,
        "below_ma20_ratio": below_ma20_ratio,
        "vkospi": vkospi,
        "ma50_support": ma50_support,
        "ma60_support": ma60_support,
        "bottom_pattern": bottom_pattern,
        "wti": wti,
        "dubai": dubai,
        "us_gdp_yoy": us_gdp_yoy,
        "us_jobs": us_jobs,
    }


# ---------------------------------------------------------------------------
# 내부 함수
# ---------------------------------------------------------------------------

def _last_trading_date() -> datetime.date:
    d = datetime.date.today()
    while d.weekday() >= 5:
        d -= datetime.timedelta(days=1)
    return d


def _fetch_yf(ticker: str, start: datetime.date, end: datetime.date) -> pd.DataFrame:
    try:
        df = yf.download(
            ticker,
            start=start.isoformat(),
            end=(end + datetime.timedelta(days=1)).isoformat(),
            progress=False,
            auto_adjust=True,
        )
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return pd.DataFrame()


def _get_yf_price(ticker: str) -> float:
    try:
        hist = yf.Ticker(ticker).history(period="5d")
        return round(float(hist["Close"].iloc[-1]), 2)
    except Exception:
        return 0.0


def _calc_vkospi(kospi_cl: pd.Series) -> float:
    """20일 연환산 역사적 변동성으로 V-KOSPI를 근사한다."""
    returns = kospi_cl.pct_change().dropna().tail(20)
    hist_vol = float(returns.std()) * (252 ** 0.5) * 100
    return round(hist_vol, 1)


def _get_below_ma20_ratio(today: datetime.date) -> float:
    """KOSPI 시총 상위 50종목 샘플로 20일 MA 하회 비율을 계산한다.

    FinanceDataReader 개별 종목 API(Yahoo Finance 백엔드) 사용.
    실패 시 50.0 반환.
    """
    try:
        import FinanceDataReader as fdr

        start = (today - datetime.timedelta(days=35)).strftime("%Y-%m-%d")
        end   = today.strftime("%Y-%m-%d")

        sample = random.sample(_KOSPI_TOP50, 30)  # 속도 절충: 30종목 샘플
        below = 0
        total = 0

        for code in sample:
            try:
                df = fdr.DataReader(code, start, end)
                if df.empty or len(df) < 20:
                    continue
                closes = df["Close"].values.astype(float)
                if closes[-1] < closes[-20:].mean():
                    below += 1
                total += 1
            except Exception:
                continue

        return round(below / total * 100, 1) if total > 0 else 50.0
    except Exception:
        return 50.0


def _detect_bottom_pattern(closes: np.ndarray) -> str:
    """가격 히스토리에서 바닥 패턴을 탐지한다."""
    if len(closes) < 20:
        return "V_attempt"

    today     = float(closes[-1])
    prev      = float(closes[-2])
    daily_chg = (today - prev) / prev * 100

    if daily_chg <= -3.0:
        return "Panic_capitulation"

    window         = closes[-40:] if len(closes) >= 40 else closes
    low_idx        = int(np.argmin(window))
    recent_low     = float(window[low_idx])
    days_since_low = len(window) - 1 - low_idx

    if 8 <= days_since_low <= 30:
        after_low    = window[low_idx:]
        mid_recovery = (float(after_low.max()) - recent_low) / recent_low * 100
        if mid_recovery > 3:
            if abs(today - recent_low) / recent_low * 100 < 3:
                return "W_second_bottom"
            return "W_forming"

    return "V_attempt"


def _get_us_macro(fred_api_key: str) -> tuple[float, str]:
    return _get_us_gdp_yoy(fred_api_key), _get_us_jobs(fred_api_key)


def _get_us_gdp_yoy(fred_api_key: str) -> float:
    if not fred_api_key:
        return 2.5
    try:
        from fredapi import Fred
        gdp = Fred(api_key=fred_api_key).get_series("GDPC1")
        if len(gdp) < 5:
            return 2.5
        return round((float(gdp.iloc[-1]) - float(gdp.iloc[-5])) / float(gdp.iloc[-5]) * 100, 1)
    except Exception:
        return 2.5


def _get_us_jobs(fred_api_key: str) -> str:
    if not fred_api_key:
        return "stable"
    try:
        from fredapi import Fred
        payroll = Fred(api_key=fred_api_key).get_series("PAYEMS")
        change = float(payroll.iloc[-1] - payroll.iloc[-2])
        if change > 250:
            return "strong"
        if change > 100:
            return "stable"
        return "weak"
    except Exception:
        return "stable"
