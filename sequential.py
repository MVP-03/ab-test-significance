"""Sequential probability ratio test (SPRT) for early stopping."""
from typing import Optional
import math


def log_likelihood_ratio(
    successes: int,
    trials: int,
    p0: float,
    p1: float,
) -> float:
    if trials == 0:
        return 0.0
    failures = trials - successes
    if p1 <= 0 or p1 >= 1 or p0 <= 0 or p0 >= 1:
        return 0.0
    ll = (
        successes * math.log(p1 / p0)
        + failures * math.log((1 - p1) / (1 - p0))
    )
    return ll


def sprt_decision(
    llr: float,
    alpha: float = 0.05,
    beta: float = 0.20,
) -> Optional[str]:
    upper = math.log((1 - beta) / alpha)
    lower = math.log(beta / (1 - alpha))
    if llr >= upper:
        return 'reject_null'
    if llr <= lower:
        return 'accept_null'
    return None


def run_sprt(
    observations: list,
    p0: float,
    p1: float,
    alpha: float = 0.05,
    beta: float = 0.20,
):
    cumulative_llr = 0.0
    for i, obs in enumerate(observations):
        s = sum(observations[:i + 1])
        cumulative_llr = log_likelihood_ratio(s, i + 1, p0, p1)
        decision = sprt_decision(cumulative_llr, alpha, beta)
        if decision:
            return {'decision': decision, 'at_observation': i + 1, 'llr': cumulative_llr}
    return {'decision': 'continue', 'at_observation': len(observations), 'llr': cumulative_llr}
