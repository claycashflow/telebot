"""
장 마감 데이터 자동 수집 모듈.

백엔드 구성:
- yfinance         : KOSPI(^KS11), WTI(CL=F), 브렌트유(BZ=F, Dubai 대체 지표), 미국 10년물(^TNX)
                     * 미국 10년물 금리는 실시간성 확보를 위해 Yahoo Finance 시장가를 최우선으로 한다.
- FinanceDataReader: KOSPI 시총 상위 50종목 개별 시세 -> below_ma20_ratio 계산
- fredapi          : 미국 GDP YoY, 고용 동향 (미 국채 금리는 Yahoo Finance 실패 시 백업용)

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

    kospi_hist = _fetch_yf("^KS11", start, today)

    if kospi_hist.empty:
        raise RuntimeError("KOSPI 데이터를 가져오지 못했다. 네트워크를 확인해주세요.")

    kospi_cl = kospi_hist["Close"].squeeze()

    kospi_close  = round(float(kospi_cl.iloc[-1]), 2)
    kospi_prev   = round(float(kospi_cl.iloc[-2]), 2)

    kospi_change_pt  = round(kospi_close - kospi_prev, 2)
    kospi_change_pct = round(kospi_change_pt / kospi_prev * 100, 2)

    # 52주 고점 대비 하락률
    kospi_52w_high = float(kospi_hist["High"].squeeze().tail(252).max())
    kospi_drawdown_pct = round((kospi_close - kospi_52w_high) / kospi_52w_high * 100, 1)

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

    # 유가. yfinance에는 Dubai 원유 지표가 없어 BZ=F를 대체 지표로 둔다.
    wti_hist = _get_yf_close_history("CL=F")
    dubai_hist = _get_yf_close_history("BZ=F")
    wti = _last_price(wti_hist, "WTI")
    dubai = _last_price(dubai_hist, "Dubai 대체 지표")
    oil_benchmark = _oil_benchmark_series(wti_hist, dubai_hist)
    oil_20d_avg = _calc_oil_20d_avg(oil_benchmark)
    oil_5d_change_pct = _calc_oil_5d_change_pct(oil_benchmark)

    # 미국 매크로
    us_gdp_yoy, us_jobs = _get_us_macro(fred_api_key)
    us_10y_yield, us_10y_source = _get_us_10y_yield(fred_api_key)

    return {
        "date": today.strftime("%Y-%m-%d"),
        "kospi_close": kospi_close,
        "kospi_change_pt": kospi_change_pt,
        "kospi_change_pct": kospi_change_pct,
        "kospi_drawdown_pct": kospi_drawdown_pct,
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
        "us_10y_yield": us_10y_yield,
        "us_10y_source": us_10y_source,
        "oil_20d_avg": oil_20d_avg,
        "oil_5d_change_pct": oil_5d_change_pct,
        "oil_data_source": "WTI=CL=F, Dubai=Brent proxy BZ=F",
        "vkospi_source": "20d historical volatility proxy",
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


def _get_yf_close_history(ticker: str, period: str = "30d") -> pd.Series:
    try:
        hist = yf.Ticker(ticker).history(period=period)
        if hist.empty:
            return pd.Series(dtype=float)
        return hist["Close"].dropna().astype(float)
    except Exception:
        return pd.Series(dtype=float)


def _last_price(series: pd.Series, label: str) -> float:
    if series.empty:
        raise RuntimeError(f"{label} 데이터를 가져오지 못했다.")
    return round(float(series.iloc[-1]), 2)


def _oil_benchmark_series(wti: pd.Series, dubai: pd.Series) -> pd.Series:
    series_list = []
    if not wti.empty:
        series_list.append(wti.rename("wti"))
    if not dubai.empty:
        series_list.append(dubai.rename("dubai"))
    if not series_list:
        return pd.Series(dtype=float)
    return pd.concat(series_list, axis=1).max(axis=1).dropna()


def _calc_oil_20d_avg(oil: pd.Series) -> float | None:
    if len(oil) < 20:
        return None
    return round(float(oil.tail(20).mean()), 1)


def _calc_oil_5d_change_pct(oil: pd.Series) -> float | None:
    if len(oil) < 6:
        return None
    prev = float(oil.iloc[-6])
    if prev <= 0:
        return None
    return round((float(oil.iloc[-1]) - prev) / prev * 100, 1)


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


def _get_us_10y_yield(fred_api_key: str) -> tuple[float | None, str]:
    """
    미국 10년물 금리(Treasury Yield 10 Years)를 수집한다.
    실시간 시장가 반영을 위해 Yahoo Finance(^TNX)를 최우선으로 하며, 실패 시 FRED(DGS10)를 백업으로 사용한다.
    """
    try:
        # 1. Yahoo Finance 시장 데이터 우선 조회
        # ^TNX는 시카고 옵션 거래소(CBOE)에서 산출하는 10년물 수익률 지수
        ticker = yf.Ticker("^TNX")
        raw = None
        
        # 실시간 세션 가격 확인
        if hasattr(ticker, 'fast_info') and 'last_price' in ticker.fast_info:
            raw = ticker.fast_info['last_price']
        
        # fast_info 실패 또는 휴장일인 경우 최근 5일 히스토리에서 마지막 유효값 추출
        if raw is None or np.isnan(raw):
            hist = ticker.history(period="5d")
            if not hist.empty:
                raw = float(hist["Close"].iloc[-1])

        if raw is not None and not np.isnan(raw):
            # Yahoo ^TNX는 금리의 10배수로 표기되는 경우가 많으므로 보정 (예: 45.4 -> 4.54)
            value = raw / 10 if raw > 20 else raw
            return round(value, 2), "Yahoo ^TNX (Real-time Market)"
    except Exception:
        pass

    if fred_api_key:
        try:
            # 2. Yahoo Finance 실패 시 FRED 백업 (전일자 종가 기준이므로 4.47% 등 지연 발생 가능)
            from fredapi import Fred
            series = Fred(api_key=fred_api_key).get_series("DGS10").dropna()
            if len(series) > 0:
                return round(float(series.iloc[-1]), 2), "FRED DGS10 (Daily/Delayed)"
        except Exception:
            pass

    return None, "missing"


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
