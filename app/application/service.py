from app.domain.judgement import evaluate_market
from app.domain.models import MarketInput
from app.domain.report import build_report
from app.domain.validator import validate_market_input


def run_market_check(payload: dict) -> tuple[MarketInput, dict, str]:
    market_input = validate_market_input(payload)
    judgement = evaluate_market(market_input)
    report = build_report(market_input, judgement)
    return market_input, judgement, report
