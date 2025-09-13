# CAFOR Parent Selection Algorithm (Python Implementation)
# Based on Algorithm 1 from the paper

class Parent:
    def __init__(self, name, etx, bo, rtmetric, is_sink=False):
        self.name = name
        self.etx = etx          # Expected Transmission Count
        self.bo = bo            # Buffer Occupancy
        self.rtmetric = rtmetric
        self.is_sink = is_sink  # True if node is sink

# Weights (from the paper: W_ETX=50, W_RtMetric=20, W_BO=4276)
W_ETX = 50
W_RtMetric = 20
W_BO = 4276

def calculate_rank(parent):
    """Compute AWSM rank for a parent."""
    return (parent.etx * W_ETX +
            parent.bo * W_BO +
            parent.rtmetric * W_RtMetric)

def select_best_parent(parents):
    """
    Select the best parent from a list of candidate parents.
    :param parents: list of Parent objects
    :return: Parent object selected as best parent
    """
    # Initialize with the first parent
    best_parent = parents[0]
    
    if best_parent.is_sink:
        return best_parent
    
    best_rank = calculate_rank(best_parent)

    # Compare with the rest
    for p in parents[1:]:
        if p.is_sink:
            return p  # Sink node always preferred
        current_rank = calculate_rank(p)
        if current_rank < best_rank:
            best_parent = p
            best_rank = current_rank

    return best_parent


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    # Example from paper matrix
    p1 = Parent("P1", etx=699, bo=0.5, rtmetric=2320)
    p2 = Parent("P2", etx=768, bo=0.625, rtmetric=2048)
    p3 = Parent("P3", etx=640, bo=0.375, rtmetric=1766)

    parents = [p1, p2, p3]

    best = select_best_parent(parents)
    print(f"Best parent selected: {best.name}, Rank = {calculate_rank(best)}")
