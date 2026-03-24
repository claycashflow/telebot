from app.domain.models import MarketInput

_SEPARATOR = "-" * 20


def build_report(data: MarketInput, judgement: dict) -> str:
    reasons = "\n".join(f"  - {r}" for r in judgement["reasons"]) or "  - 근거 없음"
    ma_support = _format_ma_support(data)
    change_arrow = _format_change_arrow(data.kospi_change_pt)
    peak = data.kospi_close / (1 + data.kospi_drawdown_pct / 100)
    ma20 = data.kospi_close * 100 / data.disparity_20

    mdd_label    = _mdd_label(data.kospi_drawdown_pct)
    disp_label   = _disparity_label(data.disparity_20)
    vkospi_label = _vkospi_label(data.vkospi)
    below_label  = _below_ma20_label(data.below_ma20_ratio)
    wti_label    = _oil_label(data.wti)
    dubai_label  = _oil_label(data.dubai)
    gdp_label    = _gdp_label(data.us_gdp_yoy)
    narrative    = _build_narrative(data, judgement)

    return (
        f"지금이뉘 - 저점인지 객관적으로 알아보기\n"
        f"📊 {data.date} 장 마감 기준\n"
        f"\n"
        f"🇰🇷 KOSPI {data.kospi_close:,.2f} {change_arrow} {abs(data.kospi_change_pt):.2f}pt ({data.kospi_change_pct:+.2f}%)\n"
        f"\n"
        f"{_SEPARATOR}\n"
        f"① 52주 고점 대비 하락률 (MDD)\n"
        f"  - 52주 최고점: {peak:,.2f}\n"
        f"  - 현재: {data.kospi_close:,.2f}\n"
        f"  - 하락률: {data.kospi_drawdown_pct:.1f}%  [기준: -18%~-23% → 저점 후보 / -23% 초과 → 침체 점검]\n"
        f"  - 평가: {mdd_label}\n"
        f"\n"
        f"② 20일 이동평균 이격도\n"
        f"  - 20일 MA: {ma20:,.2f}\n"
        f"  - 현재: {data.kospi_close:,.2f}\n"
        f"  - 이격도: {data.disparity_20:.1f}  [기준: 92 이하 → 저평가 / 88 이하 → 극단]\n"
        f"  - 평가: {disp_label}\n"
        f"\n"
        f"③ 전종목 20일 MA 하회 비율\n"
        f"  - 하회 종목: {data.below_ma20_ratio:.1f}%  [기준: 70% 이상 → 시장 과매도 구간]\n"
        f"  - 평가: {below_label}\n"
        f"\n"
        f"④ V-KOSPI (변동성)\n"
        f"  - {data.vkospi:.1f}  [기준: 40 이상 → 공포 극단 구간]\n"
        f"  - 평가: {vkospi_label}\n"
        f"\n"
        f"{_SEPARATOR}\n"
        f"🔍 저점 판독 결과\n"
        f"  - 판정: {judgement['status']}\n"
        f"  - 점수: {judgement['score']}점  [기준: 0~2 → 추가 조정 / 3~5 → 저점 근접 / 6+ → 진 바닥]\n"
        f"  - 근거:\n"
        f"{reasons}\n"
        f"\n"
        f"🌐 매크로 상황\n"
        f"  - WTI: {data.wti} ({wti_label})  /  Dubai: {data.dubai} ({dubai_label})  [기준: 80 초과 → 감점 / 100 이상 → 추가 감점]\n"
        f"  - 미국 GDP YoY: {data.us_gdp_yoy}% ({gdp_label})  [기준: 4% 이상 → 금리 인하 기대 후퇴]\n"
        f"  - 고용 동향: {data.us_jobs}\n"
        f"\n"
        f"{_SEPARATOR}\n"
        f"📝 종합 해석\n"
        f"{narrative}\n"
        f"\n"
        f"⚠️ 본 결과는 규칙 기반 판정 보조 도구이며 투자 자문이 아니다.\n"
    )


def _format_change_arrow(change_pt: float) -> str:
    if change_pt > 0:
        return "▲"
    if change_pt < 0:
        return "▼"
    return "-"


def _build_narrative(data: MarketInput, judgement: dict) -> str:
    lines = []

    # MDD 해석
    d = data.kospi_drawdown_pct
    if d > -10:
        lines.append(f"KOSPI 하락률이 {d:.1f}%로 아직 일반 조정 구간이다. 역사적 저점 후보 구간(-18%~-23%)까지 약 {abs(-18 - d):.1f}%p 이상 추가 하락 여지가 있다.")
    elif d > -18:
        lines.append(f"KOSPI 하락률이 {d:.1f}%로 의미 있는 조정 중이나, 역사적 저점 후보 구간(-18%~-23%)까지 아직 {abs(-18 - d):.1f}%p 남아 있어 추가 하락 가능성을 열어둬야 한다.")
    elif d >= -23:
        lines.append(f"KOSPI 하락률이 {d:.1f}%로 역사적 저점 후보 구간(-18%~-23%)에 진입했다. 급등 이후 1년치 하락분을 반영하는 구간으로, 기술적 바닥 형성 가능성이 높아진다.")
    else:
        lines.append(f"KOSPI 하락률이 {d:.1f}%로 일반적인 저점 구간(-23%)을 초과했다. 단순 조정이 아닌 구조적 하락 가능성을 함께 점검해야 한다.")

    # 이격도 해석
    disp = data.disparity_20
    if disp <= 88:
        lines.append(f"20일 이격도 {disp:.1f}로 과거 엔 캐리 트레이드 청산 당시(88~90)와 유사한 극단 저평가 구간이다. 기술적 바닥 확률이 매우 높은 수준이다.")
    elif disp <= 92:
        lines.append(f"20일 이격도 {disp:.1f}로 극단 저평가 구간(88~90)에 근접 중이다. 추가 하락 시 역사적 강력 매수 구간 진입이 예상된다.")

    # 바닥 패턴 해석
    pattern = data.bottom_pattern.value
    if pattern == "W_second_bottom":
        lines.append("현재 W자형 두 번째 바닥 테스트 구간이다. 첫 번째 하락이 불확실성 때문이었다면, 이번 재하락이 악재 실체를 반영하는 투매로 이어질 경우 진 바닥 확인으로 판단할 수 있다.")
    elif pattern == "Panic_capitulation":
        lines.append("당일 투매성 급락이 발생했다. 대중의 공포가 극에 달한 신호로, 역발상 관점에서 시장이 강력한 변곡점에 근접했을 가능성이 있다.")
    elif pattern == "W_forming":
        lines.append("W자형 바닥을 형성 중이다. V자 반등보다는 두 번째 바닥 확인 후 본격 반등이 역사적으로 더 신뢰도가 높았다. 두 번째 하락 확인까지 관망이 유효하다.")
    elif pattern == "V_attempt":
        lines.append("급락 후 V자 반등을 시도 중이다. 첫 반등 이후 재하락이 빈번하므로 두 번째 바닥 확인 전까지는 신중한 접근이 필요하다.")

    # V-KOSPI 해석
    vk = data.vkospi
    if vk >= 70:
        lines.append(f"V-KOSPI {vk:.1f}로 역사적 극단 공포 구간(80 근처)에 근접했다. 과거 이 수준에서는 강력한 시장 변곡점이 형성됐다.")
    elif vk >= 40:
        lines.append(f"V-KOSPI {vk:.1f}로 공포 구간에 진입했으나, 역사적 극단 수준(80 근처)까지는 아직 {80 - vk:.0f}pt 여유가 있다.")

    # 유가 리스크 해석
    if data.wti >= 100 or data.dubai >= 100:
        lines.append(f"유가(WTI {data.wti} / Dubai {data.dubai})가 100달러를 돌파했다. 인플레이션 재자극으로 금리 인하 스케줄이 무너질 수 있어 추세적 하락 리스크를 경계해야 한다.")
    elif data.wti > 80 or data.dubai > 80:
        lines.append(f"유가(WTI {data.wti} / Dubai {data.dubai})가 80달러를 초과했다. 100달러 돌파 여부가 매크로 리스크의 분수령이다.")

    # 계절성 해석
    try:
        month = int(data.date.split("-")[1])
        if month in (3, 4, 5):
            lines.append("현재 3~5월로 역사적으로 조정이 빈번한 시기다. 계절적 조정의 끝자락일 가능성을 함께 고려할 수 있다.")
        elif month in (9, 10, 11):
            lines.append("현재 9~11월로 역사적으로 조정이 빈번한 시기다. 계절적 조정의 끝자락일 가능성을 함께 고려할 수 있다.")
    except (ValueError, IndexError):
        pass

    return "\n".join(f"  {line}" for line in lines) if lines else "  현재 지표만으로는 추가 해석이 어렵다."


def _mdd_label(drawdown: float) -> str:
    if -23 <= drawdown <= -18:
        return "저점 후보 구간 진입"
    if drawdown < -23:
        return "침체/붕괴 구간 — 추가 점검 필요"
    if drawdown < -10:
        return f"의미 있는 조정 중 (저점 후보까지 {abs(-18 - drawdown):.1f}%p 남음)"
    return f"일반 조정 구간 (저점 후보까지 {abs(-18 - drawdown):.1f}%p 남음)"


def _disparity_label(disparity: float) -> str:
    if disparity <= 88:
        return "극단 과매도 구간"
    if disparity <= 92:
        return "저평가 신호 구간"
    if disparity <= 97:
        return f"중립 (저평가 기준까지 {disparity - 92:.1f}p 남음)"
    return f"평균 이상 (저평가 기준까지 {disparity - 92:.1f}p 남음)"


def _vkospi_label(vkospi: float) -> str:
    if vkospi >= 40:
        return "공포 극단 구간"
    if vkospi >= 30:
        return f"공포 확대 중 (극단 기준까지 {40 - vkospi:.1f} 남음)"
    return f"보통 수준 (극단 기준까지 {40 - vkospi:.1f} 남음)"


def _below_ma20_label(ratio: float) -> str:
    if ratio >= 70:
        return "과매도 구간 — 바닥 신호 가능성"
    if ratio >= 50:
        return f"주의 구간 (과매도 기준까지 {70 - ratio:.1f}%p 남음)"
    return "정상 범위"


def _oil_label(price: float) -> str:
    if price >= 100:
        return "고유가 위험"
    if price > 80:
        return "부담 구간"
    return "안정"


def _gdp_label(gdp: float) -> str:
    if gdp >= 4.0:
        return "금리 인하 기대 후퇴 우려"
    return "양호"


def _format_ma_support(data: MarketInput) -> str:
    supported = []
    if data.ma50_support:
        supported.append("50일")
    if data.ma60_support:
        supported.append("60일")
    return ", ".join(supported) + " 지지" if supported else "없음"
