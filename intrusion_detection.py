# intrusion_detection.py
from typing import List
from parent_selection import Parent

class SimpleIDS:
    """
    Rule-based IDS for IoT parent nodes.
    Monitors drop rate and sudden increases in drop rate.
    Updates parent.trust accordingly.
    """

    def __init__(self,
                 drop_rate_threshold: float = 0.3,
                 sudden_increase_threshold: float = 0.2,
                 trust_decrement: float = 0.25,
                 trust_increment: float = 0.05,
                 min_trust: float = 0.0,
                 max_trust: float = 1.0):
        self.drop_rate_threshold = drop_rate_threshold
        self.sudden_increase_threshold = sudden_increase_threshold
        self.trust_decrement = trust_decrement
        self.trust_increment = trust_increment
        self.min_trust = min_trust
        self.max_trust = max_trust
        # Keep historical drop rates for sudden-change detection
        self.prev_drop_rates = {}

    def inspect(self, parents: List[Parent]) -> List[str]:
        """
        Inspect list of parents, update trust values in-place.
        Returns list of detected issues as messages.
        """
        alerts = []
        for p in parents:
            current = p.drop_rate
            prev = self.prev_drop_rates.get(p.id, 0.0)

            # Rule 1: absolute drop rate too high
            if current >= self.drop_rate_threshold:
                old_trust = p.trust
                p.trust = max(self.min_trust, p.trust - self.trust_decrement)
                alerts.append(f"[ALERT] Parent {p.id} high drop rate {current:.2f} -> trust {old_trust:.2f} -> {p.trust:.2f}")

            # Rule 2: sudden increase in drop rate
            elif (current - prev) >= self.sudden_increase_threshold:
                old_trust = p.trust
                p.trust = max(self.min_trust, p.trust - (self.trust_decrement/2))
                alerts.append(f"[ALERT] Parent {p.id} sudden drop rate increase {prev:.2f}->{current:.2f} -> trust {old_trust:.2f} -> {p.trust:.2f}")

            else:
                # small reward for stable good behavior (slow trust increase)
                if current < (self.drop_rate_threshold / 2):
                    old_trust = p.trust
                    p.trust = min(self.max_trust, p.trust + self.trust_increment)
                    if p.trust != old_trust:
                        alerts.append(f"[INFO] Parent {p.id} trust increased {old_trust:.2f} -> {p.trust:.2f}")

            # persist current as prev for next round
            self.prev_drop_rates[p.id] = current

        return alerts
