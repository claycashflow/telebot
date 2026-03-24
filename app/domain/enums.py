from enum import Enum


class BottomPattern(str, Enum):
    V_ATTEMPT = "V_attempt"
    W_FORMING = "W_forming"
    W_SECOND_BOTTOM = "W_second_bottom"
    PANIC_CAPITULATION = "Panic_capitulation"


class EarningsView(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class BottomStatus(str, Enum):
    NEED_MORE_ADJUSTMENT = "추가 조정 필요"
    NEAR_BOTTOM = "저점 근접"
    TRUE_BOTTOM_CONFIRMED = "진 바닥 확인"
