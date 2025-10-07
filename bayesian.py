"""Bayesian A/B test analysis using Beta-Binomial model."""
from typing import Tuple
import math


def beta_mean(alpha: float, beta: float) -> float:
    return alpha / (alpha + beta)


def beta_variance(alpha: float, beta: float) -> float:
    ab = alpha + beta
    return (alpha * beta) / (ab * ab * (ab + 1))


def posterior(successes: int, trials: int, prior_alpha: float = 1.0, prior_beta: float = 1.0) -> Tuple[float, float]:
    return prior_alpha + successes, prior_beta + (trials - successes)


def prob_b_beats_a(
    a_successes: int, a_trials: int,
    b_successes: int, b_trials: int,
    samples: int = 10_000,
) -> float:
    import random
    a_alpha, a_beta = posterior(a_successes, a_trials)
    b_alpha, b_beta = posterior(b_successes, b_trials)

    wins = 0
    for _ in range(samples):
        a_sample = random.betavariate(a_alpha, a_beta)
        b_sample = random.betavariate(b_alpha, b_beta)
        if b_sample > a_sample:
            wins += 1
    return round(wins / samples, 4)


def expected_loss(
    a_successes: int, a_trials: int,
    b_successes: int, b_trials: int,
    samples: int = 10_000,
) -> Tuple[float, float]:
    import random
    a_alpha, a_beta = posterior(a_successes, a_trials)
    b_alpha, b_beta = posterior(b_successes, b_trials)

    loss_a, loss_b = 0.0, 0.0
    for _ in range(samples):
        a_s = random.betavariate(a_alpha, a_beta)
        b_s = random.betavariate(b_alpha, b_beta)
        loss_a += max(b_s - a_s, 0)
        loss_b += max(a_s - b_s, 0)
    return round(loss_a / samples, 6), round(loss_b / samples, 6)
