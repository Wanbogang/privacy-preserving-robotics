# Examples and Demonstrations

This directory contains working demonstrations of the Privacy-Preserving Home Robotics Framework.

## 🎯 Available Demos

### 1. Ephemeral Identity Management
**File**: `ephemeral_identity_demo.py`  
**Runtime**: ~10 seconds  
**Pillar**: Identity without Identification

Demonstrates how the system recognizes and tracks entities through behavioral patterns without biometric identification.

**Run:**
```bash
python3 ephemeral_identity_demo.py
```

**What it shows:**
- Entity detection and re-identification
- Behavioral similarity matching
- Confidence building over observations
- Entity discrimination (Person A vs Person B)
- Privacy properties verification

---

### 2. Pattern Memory System
**File**: `pattern_memory_demo.py`  
**Runtime**: ~30 seconds  
**Pillar**: Memory without Recording

Demonstrates how the system learns behavioral patterns through statistical summarization without storing event logs.

**Run:**
```bash
python3 pattern_memory_demo.py
```

**What it shows:**
- Learning daily routines over 2 weeks
- Statistical pattern storage (means, std deviations)
- Temporal and spatial pattern learning
- Anomaly detection (10.54σ deviation examples)
- Privacy proof: cannot reconstruct Day 3's events
- Exponential decay forgetting mechanism

---

### 3. Eldercare Fall Detection (Complete Scenario)
**File**: `eldercare_fall_detection.py`  
**Runtime**: ~60 seconds  
**Pillars**: Complete system integration

Demonstrates a complete privacy-preserving eldercare monitoring system combining ephemeral identity and pattern memory.

**Run:**
```bash
python3 eldercare_fall_detection.py
```

**What it shows:**
- **Phase 1**: Pattern learning over 3 days
  - Morning, midday, evening routines
  - Active hours: [7, 12, 18, 19]
  
- **Phase 2**: Fall detection scenario
  - Pressure sensor detects sudden impact
  - 0.85 confidence alert
  - Emergency response without video
  
- **Phase 3**: Inactivity detection
  - 65 minutes no movement during active hours
  - 0.95 confidence anomaly alert
  - Pattern-based wellness check

- **Privacy verification report**
  - No biometric storage
  - Cannot reconstruct specific events
  - Effective safety without surveillance

---

## 🔧 Requirements

All demos require:
```bash
pip install numpy scipy matplotlib tabulate
```

Or install from root directory:
```bash
cd ..
pip install -r requirements.txt
```

---

## 📊 Understanding the Output

### Privacy Verification Checklist

Every demo verifies these privacy properties:

✓ **No Biometric Data**: No faces, voiceprints, fingerprints stored  
✓ **No Event Logs**: No timestamped activity records  
✓ **No Reconstruction**: Cannot recreate specific past events  
✓ **Ephemeral IDs**: Temporary identifiers that expire  
✓ **Pattern-Based**: Only statistical summaries maintained  

### Key Metrics

- **Confidence scores**: How certain the system is (0.0-1.0)
- **Deviation (σ)**: Standard deviations from learned patterns
  - < 2σ: Normal behavior
  - 2-3σ: Unusual but not alarming
  - > 3σ: Significant anomaly, may trigger alert
- **Observation counts**: How many times a pattern has been seen

---

## 🎓 Learning Path

**Recommended order:**

1. **Start with `ephemeral_identity_demo.py`**
   - Understand how identity works without biometrics
   - See behavioral matching in action
   - Grasp the core privacy principle

2. **Then `pattern_memory_demo.py`**
   - Learn how memory works without recording
   - Understand statistical pattern storage
   - See anomaly detection

3. **Finally `eldercare_fall_detection.py`**
   - See complete system integration
   - Understand real-world application
   - Observe emergency response scenarios

---

## 💡 Extending the Demos

### Modify Parameters

Each demo has tunable parameters at the top:
```python
# In ephemeral_identity_demo.py
manager = EphemeralIdentityManager(
    similarity_threshold=0.85,  # Try 0.70 for stricter matching
    expiry_days=30              # Try 7 for faster expiration
)

# In pattern_memory_demo.py
memory = PatternMemory(
    decay_factor=0.98  # Try 0.95 for faster forgetting
)

# In eldercare_fall_detection.py
monitor.inactivity_threshold_minutes = 30  # Try 60 for more tolerance
```

### Add Your Own Scenarios

Use these demos as templates:

1. Copy a demo file
2. Modify the simulation functions
3. Add new sensor types or behaviors
4. Test privacy properties still hold

---

## 🐛 Troubleshooting

**Import errors?**
```bash
pip install -r ../requirements.txt
```

**Demo runs too fast?**
Edit the `time.sleep()` values in the code to slow down output.

**Want more detail?**
Check the source code comments for implementation details.

---

## 📞 Questions?

- Check main [README](../README.md)
- Read [Documentation](../docs/)
- Open [GitHub Issue](https://github.com/Wanbogang/privacy-preserving-robotics/issues)
- Email: harapan.bontang@gmail.com

---

**Remember**: These demos prove privacy and functionality are NOT mutually exclusive!
