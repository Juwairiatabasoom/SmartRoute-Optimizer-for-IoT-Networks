# network_demo.py
import random
import time
from parent_selection import Parent, select_best_parent, calculate_rank
from intrusion_detection import SimpleIDS

def simulate_round(parents, malicious_id=None, mal_drop_prob=0.8):
    """
    Simulate sending 100 packets to each parent and randomly decide delivered/dropped.
    If malicious_id set, that parent will drop packets at mal_drop_prob.
    """
    for p in parents:
        # simulate variable ETX and BO jitter as network changes
        p.etx = max(1.0, p.etx + random.uniform(-10, 10))
        p.bo = min(max(0.0, p.bo + random.uniform(-0.05, 0.05)), 1.0)
        p.rtmetric = max(1.0, p.rtmetric + random.uniform(-50, 50))

        packets = 100
        p.record_sent(packets)
        # If it's malicious, drop with higher probability
        if p.id == malicious_id:
            dropped = int(packets * mal_drop_prob)
        else:
            # healthy nodes drop small random proportion
            dropped = int(packets * random.uniform(0.0, 0.05))

        delivered = packets - dropped
        p.record_dropped(dropped)
        p.record_delivered(delivered)

def pretty_status(parents):
    print("Parent status:")
    for p in parents:
        print(f"  {p.id:>3} | ETX: {p.etx:6.1f} | BO: {p.bo:.3f} | Rt: {p.rtmetric:6.1f} | trust: {p.trust:.2f} | drop: {p.drop_rate:.2f} | rank: {calculate_rank(p):.1f}")

def reset_stats(parents):
    for p in parents:
        p.stats = {"sent": 0, "delivered": 0, "dropped": 0}

def demo():
    # Create sample parents
    p1 = Parent("P1", etx=699, bo=0.5, rtmetric=2320)
    p2 = Parent("P2", etx=768, bo=0.625, rtmetric=2048)
    p3 = Parent("P3", etx=640, bo=0.375, rtmetric=1766)
    p4 = Parent("P4", etx=300, bo=0.2, rtmetric=900)  # initially attractive

    parents = [p1, p2, p3, p4]

    ids = SimpleIDS(drop_rate_threshold=0.2, sudden_increase_threshold=0.15, trust_decrement=0.3, trust_increment=0.05)

    print("\n=== EdgeFlow-Sec Demo: trust-aware parent selection with IDS ===\n")

    # Warm-up rounds (normal operation)
    for round_no in range(1, 4):
        print(f"\n--- Round {round_no} (normal) ---")
        simulate_round(parents)   # no attacker
        alerts = ids.inspect(parents)
        for a in alerts:
            print(a)
        pretty_status(parents)
        best = select_best_parent(parents)
        print(f">>> Selected best parent: {best.id} (trust {best.trust:.2f})")
        time.sleep(0.2)

    # Now simulate attack: P4 becomes malicious with high drop prob and artificially low ETX/BO to lure traffic
    print("\n--- Attack: P4 becomes a sinkhole (lures traffic then drops) ---")
    reset_stats(parents)

    # Over several rounds attacker remains active
    for round_no in range(4, 9):
        # artificially make P4 appear attractive in metrics
        p4 = next(p for p in parents if p.id == "P4")
        p4.etx = random.uniform(50, 150)   # low ETX to lure
        p4.bo = random.uniform(0.05, 0.15)
        p4.rtmetric = random.uniform(400, 1000)

        print(f"\n--- Round {round_no} (attack active) ---")
        simulate_round(parents, malicious_id="P4", mal_drop_prob=0.75)
        alerts = ids.inspect(parents)
        for a in alerts:
            print(a)
        pretty_status(parents)
        best = select_best_parent(parents)
        print(f">>> Selected best parent: {best.id} (trust {best.trust:.2f})")
        time.sleep(0.2)

    print("\n--- Post-attack: attacker removed / trust restored slowly ---")
    reset_stats(parents)
    # attacker stops but has low trust; see if trust recovers
    for round_no in range(9, 13):
        print(f"\n--- Round {round_no} (post-attack) ---")
        simulate_round(parents)  # no attacker now
        alerts = ids.inspect(parents)
        for a in alerts:
            print(a)
        pretty_status(parents)
        best = select_best_parent(parents)
        print(f">>> Selected best parent: {best.id} (trust {best.trust:.2f})")
        time.sleep(0.2)

if __name__ == "__main__":
    demo()
