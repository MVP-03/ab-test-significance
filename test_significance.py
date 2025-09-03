import pytest
from significance import z_test_two_proportions, lift


def test_significant_difference():
    z, p, conclusion = z_test_two_proportions(50, 500, 90, 500)
    assert p < 0.05
    assert 'significant' in conclusion


def test_no_difference():
    z, p, conclusion = z_test_two_proportions(50, 500, 51, 500)
    assert p > 0.10
    assert 'not significant' in conclusion


def test_zero_sample_size_raises():
    with pytest.raises(ValueError):
        z_test_two_proportions(0, 0, 10, 100)


def test_conversions_exceed_n_raises():
    with pytest.raises(ValueError):
        z_test_two_proportions(110, 100, 10, 100)


def test_lift_positive():
    assert lift(0.10, 0.15) == 50.0


def test_lift_negative():
    assert lift(0.15, 0.10) == round(-33.3, 1)


def test_lift_zero_control():
    assert lift(0.0, 0.10) == 0.0


def test_p_value_below_0_01():
    z, p, conclusion = z_test_two_proportions(10, 500, 80, 500)
    assert p < 0.01
    assert '99%' in conclusion
