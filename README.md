# SmartRoute-Optimizer-for-IoT-Networks

EdgeFlow-Sec is a **cybersecurity-focused IoT routing system** that extends the CAFOR algorithm (Congestion Avoidance using Fuzzy Logic for Optimal Routing).  
It combines **fuzzy-logic–based parent selection** with a **lightweight Intrusion Detection System (IDS)** to protect against malicious routing behaviors such as **sinkhole or selective forwarding attacks** in 6LoWPAN IoT networks.  

---

## 🚀 Features
- **Fuzzy Weighted Sum Model (FWSM)** for parent selection  
- Considers **ETX (Expected Transmission Count)**, **Buffer Occupancy (BO)**, and **RtMetric**  
- **Trust-aware routing** → malicious nodes are penalized/excluded  
- **Intrusion Detection System (IDS)** monitors packet drops and sudden anomalies  
- **Automatic mitigation** → system avoids compromised parents during attack  
- **Attack simulation** (sinkhole node dropping packets but advertising good metrics)  
- **Recovery mechanism** → trust is gradually restored once the node behaves normally  

---

## 📂 Project Structure & File Details

- **`parent_selection.py`**  
  - Defines the **Parent class** (ETX, BO, RtMetric, trust, stats).  
  - Implements the **fuzzy logic rank calculation** from CAFOR.  
  - Adds **trust-aware parent selection** (ignores low-trust parents or penalizes them).  
  - Core engine of the project.  

- **`intrusion_detection.py`**  
  - Implements a **Simple Intrusion Detection System (IDS)**.  
  - Monitors each parent’s **packet drop rates**.  
  - Detects anomalies (high drop rate, sudden spikes).  
  - Updates each parent’s **trust score** up or down.  
  - Ensures malicious parents lose trust and get excluded.  

- **`network_demo.py`**  
  - The **driver script / simulator**.  
  - Creates parent nodes (`P1, P2, P3, P4`).  
  - Runs multiple rounds of simulation:  
    1. **Normal operation** (all good).  
    2. **Attack phase** (one node becomes malicious sinkhole).  
    3. **Recovery phase** (attack stops, trust slowly rises).  
  - Calls both the **IDS** and the **parent selection algorithm** each round.  
  - Prints detailed logs showing: ETX, BO, RtMetric, trust, drop rates, and chosen parent.  

- **`requirements.txt`**  
  - Lists optional dependencies (e.g., `cryptography` for adding encryption).  
  - Not strictly required for the demo, but useful for future security features.  

---

## ⚙️ Installation & Setup
```bash
# Clone repo
git clone https://github.com/your-username/edgeflow-sec.git
cd edgeflow-sec

# (Optional) create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run demo simulation
python network_demo.py
