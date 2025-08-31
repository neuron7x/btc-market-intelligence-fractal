"""First generation signal calculation utilities."""

from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
import logging
from btcmi.utils import is_number
from btcmi.config import NORM_SCALE, SCENARIO_WEIGHTS
from btcmi.feature_processing import normalize_features, weighted_score


FeatureMap = Dict[str, float]


logger = logging.getLogger(__name__)


@dataclass
class BaseSignalResult:
    """Container for :func:`base_signal` outputs."""

    score: float
    weights: FeatureMap
    contributions: FeatureMap

def normalize(features: FeatureMap) -> FeatureMap:
    """Scale raw feature values using hyperbolic tangent."""

    return normalize_features(features, NORM_SCALE)


def completeness(features: FeatureMap) -> float:
    """Compute fraction of expected features present with numeric values.

    Args:
        features: Mapping of provided features.

    Returns:
        The proportion of expected features that are present and numeric.

    """
    exp = set(NORM_SCALE.keys())
    pres = {k for k, v in features.items() if k in exp and is_number(v)}
    return len(pres) / len(exp) if exp else 1.0


def base_signal(scenario: str, norm: FeatureMap) -> BaseSignalResult:
    """Calculate weighted signal for a trading scenario.

    Args:
        scenario: Scenario key selecting the weight profile.
        norm: Normalized feature values.

    Returns:
        :class:`BaseSignalResult` with overall score, applied weights, and
        individual contributions.

    """
    weights = SCENARIO_WEIGHTS[scenario]
    score, contrib = weighted_score(norm, weights)
    return BaseSignalResult(score, weights, contrib)


def nagr_score(nodes: Any) -> float:
    """Aggregate a network graph rating score.

    Args:
        nodes: Iterable of node dictionaries with ``weight`` and ``score``.

    Returns:
        Weighted average score clipped to [-1, 1].

    """
    if not nodes:
        return 0.0
    num = 0.0
    den = 0.0
    for n in nodes:
        try:
            w = float(n.get("weight", 0.0))
            sc = float(n.get("score", 0.0))
        except (TypeError, ValueError) as exc:
            logger.debug("Skipping node with non-numeric data %s: %s", n, exc)
            continue
        num += w * sc
        den += abs(w)
    return max(-1.0, min(1.0, num / den if den else 0.0))


def combine(base: float, nagr: float) -> float:
    """Blend base and network scores.

    Args:
        base: Baseline signal score.
        nagr: Network aggregated score.

    Returns:
        Weighted combination clipped to [-1, 1].

    """
    return max(-1.0, min(1.0, 0.7 * base + 0.3 * nagr))
