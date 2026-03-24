from app.domain.models import MarketInput


def build_report(data: MarketInput, judgement: dict) -> str:
    reasons = "\n".join(f"- {reason}" for reason in judgement["reasons"]) or "- 근거 없음"
    sectors = _suggest_sectors(data)

    return (
        f"현 시점 저점 판독 결과\n"
        f"- 상태: {judgement['status']}\n"
        f"- 점수: {judgement['score']}\n\n"
        f"판단 근거 (데이터 분석)\n"
        f"{reasons}\n\n"
        f"매크로 상황 분석\n"
        f"- WTI: {data.wti}\n"
        f"- Dubai: {data.dubai}\n"
        f"- 미국 GDP YoY: {data.us_gdp_yoy}\n\n"
        f"최종 투자 의견\n"
        f"- 본 결과는 투자 판단 보조용이며 투자 자문이 아니다.\n"
        f"- 규칙 기반 판정상 현재 상태는 '{judgement['status']}'이다.\n\n"
        f"주목할 업종\n"
        f"- {sectors}\n"
    )


def _suggest_sectors(data: MarketInput) -> str:
    if data.semiconductor_earnings_view.value == "positive":
        return "반도체"
    return "근거가 충분한 업종 신호 없음"
