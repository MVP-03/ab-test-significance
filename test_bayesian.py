from bayesian import beta_mean, beta_variance, posterior, prob_b_beats_a
from sequential import log_likelihood_ratio, sprt_decision, run_sprt


def test_beta_mean():
    assert beta_mean(2, 2) == 0.5


def test_posterior_updates_alpha():
    a, b = posterior(10, 100)
    assert a == 11.0
    assert b == 91.0


def test_prob_b_beats_a_clear_winner():
    p = prob_b_beats_a(
        a_successes=10, a_trials=100,
        b_successes=40, b_trials=100,
        samples=5000,
    )
    assert p > 0.90


def test_prob_b_beats_a_near_equal():
    p = prob_b_beats_a(
        a_successes=50, a_trials=100,
        b_successes=51, b_trials=100,
        samples=5000,
    )
    assert 0.3 < p < 0.7


def test_llr_zero_trials():
    assert log_likelihood_ratio(0, 0, 0.1, 0.2) == 0.0


def test_sprt_reject():
    observations = [1] * 50 + [0] * 10
    result = run_sprt(observations, p0=0.5, p1=0.7)
    assert result['decision'] in ('reject_null', 'continue')


def test_sprt_decision_upper():
    assert sprt_decision(10.0, alpha=0.05, beta=0.20) == 'reject_null'


def test_sprt_decision_lower():
    assert sprt_decision(-10.0, alpha=0.05, beta=0.20) == 'accept_null'
