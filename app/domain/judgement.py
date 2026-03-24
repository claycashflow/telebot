from app.domain.enums import BottomPattern, BottomStatus
from app.domain.models import MarketInput


def evaluate_market(data: MarketInput) -> dict:
    score = 0
    reasons: list[str] = []
    worst_drawdown = min(data.kospi_drawdown_pct, data.kosdaq_drawdown_pct)

    if -23 <= worst_drawdown <= -18:
        score += 3
        reasons.append("하락률이 기술적 저점 후보 구간이다.")
    elif worst_drawdown < -23:
        reasons.append("하락률이 깊어 침체 가능성도 함께 점검해야 한다.")

    if data.disparity_20 <= 92 or data.disparity_60 <= 92:
        score += 2
        reasons.append("이격도가 저평가 신호 구간이다.")
    if data.disparity_20 <= 88 or data.disparity_60 <= 88:
        score += 1
        reasons.append("이격도가 극단 구간에 근접한다.")

    if data.vkospi >= 40:
        score += 2
        reasons.append("변동성이 높아 공포 확대로 해석할 수 있다.")
    if data.vkospi >= 70:
        score += 1
        reasons.append("V-KOSPI가 극단 공포 구간(70+)으로 역사적 변곡점 가능성이 높아진다.")

    if data.ma50_support or data.ma60_support:
        score += 1
        reasons.append("이동평균선 지지 신호가 있다.")

    if data.bottom_pattern in {BottomPattern.W_SECOND_BOTTOM, BottomPattern.PANIC_CAPITULATION}:
        score += 2
        reasons.append("바닥 패턴 신호가 강화되고 있다.")

    if data.wti > 80 or data.dubai > 80:
        score -= 2
        reasons.append("유가 부담이 있어 감점 요인이다.")
    if data.wti >= 100 or data.dubai >= 100:
        score -= 1
        reasons.append("유가가 높은 수준으로 추가 감점 구간이다.")

    if data.us_gdp_yoy >= 4.0:
        score -= 2
        reasons.append("미국 GDP가 높아 금리 인하 기대 후퇴 우려가 있다.")

    if score >= 6:
        status = BottomStatus.TRUE_BOTTOM_CONFIRMED
    elif score >= 3:
        status = BottomStatus.NEAR_BOTTOM
    else:
        status = BottomStatus.NEED_MORE_ADJUSTMENT

    return {"status": status.value, "score": score, "reasons": reasons}
