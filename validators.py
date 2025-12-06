from typing import Dict, List


def validate_variant(variant: Dict) -> List[str]:
    errors = []
    if variant.get('trials', 0) <= 0:
        errors.append('trials must be positive')
    successes = variant.get('successes', -1)
    trials    = variant.get('trials', 0)
    if successes < 0:
        errors.append('successes must be >= 0')
    if successes > trials:
        errors.append('successes cannot exceed trials')
    return errors


def validate_ab_test(control: Dict, treatment: Dict) -> List[str]:
    return validate_variant(control) + validate_variant(treatment)
