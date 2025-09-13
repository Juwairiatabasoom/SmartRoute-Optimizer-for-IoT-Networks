# SmartRoute-Optimizer-for-IoT-Networks
implements a fuzzy logic–based parent selection algorithm for 6LoWPAN IoT networks, achieving higher throughput, lower latency, and energy-efficient routing compared to standard RPL.

SmartRoute is an **intelligent routing system for IoT (6LoWPAN) networks** that uses **fuzzy logic** to avoid congestion and optimize parent selection.  
By dynamically selecting the least congested routing path, EdgeFlow improves **throughput, latency, energy efficiency, and reliability** compared to standard RPL protocols.

---

## 🚀 Features
- **Fuzzy Weighted Sum Model (FWSM)** for parent selection  
- Considers **Expected Transmission Count (ETX)**, **Buffer Occupancy (BO)**, and **RtMetric**  
- Proactively avoids congestion instead of reacting after failures  
- Achieves:
  - 15% higher throughput  
  - 10% higher goodput  
  - 4.5% fewer packet losses  
  - 10% lower energy consumption  
  - 19% lower end-to-end delay  

---
---

## 📝 Code Overview

The core algorithm is implemented in **`parent_selection.py`**, based directly on the CAFOR (Fuzzy Weighted Sum Model) approach.

### 🔹 Key Files
- `parent_selection.py` → Implements the **Parent class**, ranking function, and best-parent selection algorithm.  
- `network_demo.py` → Example simulation with multiple parents to show how the algorithm selects the optimal path.  

### 🔹 Algorithm (simplified)
```python
# Rank calculation
Rank = (ETX * W_ETX) + (BO * W_BO) + (RtMetric * W_RtMetric)

# Best parent = one with the lowest rank


