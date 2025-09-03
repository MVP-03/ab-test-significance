import json
import math
import sys
from typing import Tuple


def z_test_two_proportions(
    conversions_a: int,
    n_a: int,
    conversions_b: int,
    n_b: int,
) -> Tuple[float, float, str]:
    if n_a <= 0 or n_b <= 0:
        raise ValueError('sample sizes must be positive')
    if conversions_a > n_a or conversions_b > n_b:
        raise ValueError('conversions cannot exceed sample size')

    p_a = conversions_a / n_a
    p_b = conversions_b / n_b
    p_pool = (conversions_a + conversions_b) / (n_a + n_b)

    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    if se == 0:
        return 0.0, 1.0, 'no variance - both rates identical'

    z = (p_b - p_a) / se

    # two-tailed p-value approximation using error function
    p_value = 2 * (1 - _norm_cdf(abs(z)))

    if p_value < 0.01:
        conclusion = 'significant at 99% confidence'
    elif p_value < 0.05:
        conclusion = 'significant at 95% confidence'
    elif p_value < 0.10:
        conclusion = 'significant at 90% confidence - marginal'
    else:
        conclusion = 'not significant - could be noise'

    return round(z, 3), round(p_value, 4), conclusion


def _norm_cdf(z: float) -> float:
    return (1.0 + math.erf(z / math.sqrt(2))) / 2.0


def lift(rate_a: float, rate_b: float) -> float:
    if rate_a == 0:
        return 0.0
    return round((rate_b - rate_a) / rate_a * 100, 1)


def run_from_file(path: str) -> None:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    variants = data.get('variants', [])
    if len(variants) < 2:
        print('Need at least 2 variants.')
        return

    control = variants[0]
    print(f"\n  Experiment: {data.get('name', 'unnamed')}")
    print(f"  Metric:     {data.get('metric', 'conversion')}")
    print(f"  Control:    {control['name']} ({control['conversions']}/{control['n']})\n")

    for variant in variants[1:]:
        z, p, conclusion = z_test_two_proportions(
            control['conversions'], control['n'],
            variant['conversions'], variant['n'],
        )
        rate_a = control['conversions'] / control['n']
        rate_b = variant['conversions'] / variant['n']
        print(f"  Variant:  {variant['name']}")
        print(f"    Control rate:  {rate_a * 100:.2f}%")
        print(f"    Variant rate:  {rate_b * 100:.2f}%")
        print(f"    Lift:          {lift(rate_a, rate_b):+.1f}%")
        print(f"    Z-score:       {z}")
        print(f"    P-value:       {p}")
        print(f"    Result:        {conclusion}")
        print()


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'sample_data.json'
    run_from_file(path)
