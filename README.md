# ab-test-significance

Single-file Python utility for testing statistical significance of email sequence A/B experiments. No external dependencies — uses only stdlib math.

## Usage

```bash
python significance.py sample_data.json
pytest test_significance.py
```

## Sample output

```
  Experiment: Q3 Outbound Subject Line Test
  Metric:     reply_rate
  Control:    Control - question subject (48/420)

  Variant:  Variant A - pain point subject
    Control rate:  11.43%
    Variant rate:  17.11%
    Lift:          +49.7%
    Z-score:       2.981
    P-value:       0.0029
    Result:        significant at 99% confidence
```

## Input format

```json
{
  "name": "experiment name",
  "metric": "reply_rate",
  "variants": [
    { "name": "Control", "conversions": 48, "n": 420 },
    { "name": "Variant A", "conversions": 71, "n": 415 }
  ]
}
```

## Motivation

We were running 3-way subject line tests and calling winners based on raw reply rates with sample sizes under 100. This script applies a proper two-proportion z-test and flags marginal results so we stop making decisions on noise.
