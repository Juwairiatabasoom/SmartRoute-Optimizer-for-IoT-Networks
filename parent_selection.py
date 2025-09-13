# parent_selection.py
from dataclasses import dataclass, field
from typing import List

# Weights (same style as paper; tune as needed)
W_ETX = 50
W_RTMETRIC = 20
W_BO = 4276

# Trust thresholds
MIN_TRUST_TO_CONSIDER = 0.4    # below this, parent is ignored
TRUST_PENALTY_FACTOR = 1.0     # used to adjust rank by trust

@dataclass
class Parent:
    id: str
    etx: float
    bo: float
    rtmetric: float
    is_sink: bool = False
    trust: float = 1.0         # 0.0 (untrusted) to 1.0 (fully trusted)
    stats: dict = field(default_factory=lambda: {"sent": 0, "delivered": 0, "dropped": 0})

    @property
    def drop_rate(self) -> float:
        s = self.stats["sent"]
        if s == 0:
            return 0.0
        return self.stats["dropped"] / s

    def record_sent(self, n=1):
        self.stats["sent"] += n

    def record_delivered(self, n=1):
        self.stats["delivered"] += n

    def record_dropped(self, n=1):
        self.stats["dropped"] += n

def calculate_rank(parent: Parent) -> float:
    """
    Base rank calculation (FWSM style), then adjust by trust.
    Lower rank = better parent.
    We divide by (trust + eps) so higher trust reduces effective rank.
    """
    base_rank = parent.etx * W_ETX + parent.bo * W_BO + parent.rtmetric * W_RTMETRIC
    eps = 1e-6
    trust_factor = max(parent.trust, 0.01)  # avoid division by zero and keep some penalty
    rank = base_rank / (trust_factor * TRUST_PENALTY_FACTOR + eps)
    return rank

def select_best_parent(parents: List[Parent]) -> Parent:
    """
    Select the best parent considering trust.
    Sink node gets immediate priority.
    Parents below MIN_TRUST_TO_CONSIDER are excluded (mitigation).
    """
    # Prefer sink
    for p in parents:
        if p.is_sink:
            return p

    # Filter out low-trust parents
    candidates = [p for p in parents if p.trust >= MIN_TRUST_TO_CONSIDER]
    if not candidates:
        # if all parents are low-trust, fallback to highest trust
        candidates = sorted(parents, key=lambda x: x.trust, reverse=True)
        # but still return one
        return candidates[0]

    # Compute ranks and pick lowest
    best = min(candidates, key=calculate_rank)
    return best
