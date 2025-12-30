# Architecture Documentation

## System Overview

The Privacy-Preserving Robotics framework consists of six main layers that work together to provide robot functionality without surveillance.

## Layer Architecture

```
┌─────────────────────────────────────┐
│      1. Sensor Layer (Non-ID)       │
│  LiDAR, Depth, Thermal, Pressure    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   2. Feature Extraction (Immediate) │
│  Raw data discarded after features  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   3. Ephemeral Identity Management  │
│  Behavioral continuity, not ID      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    4. Pattern Memory System         │
│  Abstract patterns, no event logs   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   5. Context Understanding Engine   │
│  Anomaly detection, situation assess│
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   6. Action & Explanation Module    │
│  Execute, explain, learn feedback   │
└─────────────────────────────────────┘
```

---

## 1. Sensor Layer

### Purpose
Gather environmental context without identifiable data

### Allowed Sensors
- **LiDAR**: Spatial awareness, distance measurement
- **Depth Cameras**: Presence detection without faces
- **Thermal Sensors**: Human detection via heat signature
- **Pressure Sensors**: Movement, falls, positioning
- **Audio Amplitude**: Distress sounds (not speech content)

### Prohibited Sensors
- ❌ RGB cameras capable of facial recognition
- ❌ Speech recording microphones
- ❌ Biometric scanners (fingerprint, iris, etc.)

### Key Principle
Select sensors that provide context without enabling identification.

---

## 2. Feature Extraction Layer

### Purpose
Convert raw sensor data to abstract, non-identifiable features immediately

### Process Flow
```
raw_sensor_data → feature_extraction() → abstract_features
                                       ↓
                                  discard(raw_data)
```

### Examples

**Depth Camera:**
```
Input: Depth image array
Output: "human-like shape at position (x,y), height ~170cm"
Discard: Original depth image
```

**Thermal Sensor:**
```
Input: Thermal reading grid
Output: "heat signature consistent with human presence, zone A"
Discard: Raw thermal data
```

**Audio:**
```
Input: Audio waveform
Output: "loud sound event detected, amplitude >80dB"
Discard: Audio recording
```

### Critical Property
Raw sensor data must be discarded within **milliseconds**. No buffering, no temporary storage.

---

## 3. Ephemeral Identity Management

### Purpose
Maintain entity continuity without biometric identification

### Algorithm

```python
def assign_entity_id(behavioral_features):
    """
    Assign or retrieve entity ID based on behavioral matching
    """
    # Check for recent similar entities
    candidates = find_similar_entities(
        features=behavioral_features,
        time_window=RECENT_WINDOW  # e.g., 24 hours
    )
    
    if not candidates:
        # New entity detected
        entity_id = generate_ephemeral_id()
        initialize_pattern_profile(entity_id)
        return entity_id
    else:
        # Re-identification through behavior
        entity_id = match_behavioral_pattern(candidates, behavioral_features)
        update_pattern_profile(entity_id, behavioral_features)
        return entity_id

def generate_ephemeral_id():
    """
    Generate cryptographically random, non-sequential ID
    """
    import secrets
    return f"entity_{secrets.token_hex(16)}"

def find_similar_entities(features, time_window):
    """
    Find entities with similar behavioral patterns
    """
    recent_entities = get_entities_within_window(time_window)
    
    similar = []
    for entity in recent_entities:
        similarity = calculate_behavioral_similarity(
            entity.pattern,
            features
        )
        if similarity > SIMILARITY_THRESHOLD:
            similar.append((entity, similarity))
    
    return sorted(similar, key=lambda x: x[1], reverse=True)
```

### Key Properties
- IDs are **cryptographically random** (not sequential)
- IDs **expire** after inactivity period (e.g., 30 days)
- Re-identification based on **behavior**, not biometrics
- Significant behavioral change → new ID (privacy to evolve)

---

## 4. Pattern Memory System

### Purpose
Store behavioral patterns without event logs

### Data Structure

```python
class PatternMemory:
    def __init__(self, entity_id):
        self.entity_id = entity_id  # ephemeral
        
        # Temporal patterns
        self.temporal_patterns = {
            'active_hours': [],  # [(start, end, confidence)]
            'typical_duration': {},  # {location: (mean, std)}
            'routine_variance': 0.0
        }
        
        # Spatial patterns
        self.spatial_patterns = {
            'common_zones': [],  # [(zone_id, frequency)]
            'movement_speed': (0.0, 0.0),  # (mean, std)
            'interaction_areas': []
        }
        
        # Interaction patterns
        self.interaction_patterns = {
            'assistance_acceptance': {},  # {context: rate}
            'preferences': {},  # {type: score}
            'communication_style': {}
        }
        
        # Metadata
        self.metadata = {
            'first_observed': None,  # relative timestamp
            'last_updated': None,
            'confidence_level': 0.0,
            'pattern_stability': 0.0
        }
```

### What Is NOT Stored
- ❌ Individual events
- ❌ Timestamps of specific actions
- ❌ Raw sensor readings
- ❌ Reconstructable observations
- ❌ Biometric data
- ❌ Personal identifiable information

### Update Mechanism

```python
def update_pattern(entity_id, new_observation):
    """
    Update pattern with statistical aggregation, not event append
    """
    pattern = get_pattern(entity_id)
    
    # Update temporal pattern
    pattern.temporal_patterns['active_hours'] = update_distribution(
        current=pattern.temporal_patterns['active_hours'],
        new_data=new_observation.time,
        decay_factor=TIME_DECAY
    )
    
    # Old specific events forgotten through decay
    # Only abstract pattern remains
    
    save_pattern(entity_id, pattern)
    # NO storage of new_observation itself

def update_distribution(current, new_data, decay_factor):
    """
    Statistical update with exponential decay of old data
    """
    # Apply decay to existing distribution
    decayed = apply_decay(current, decay_factor)
    
    # Incorporate new observation
    updated = incorporate_new_data(decayed, new_data)
    
    return updated
```

---

## 5. Context Understanding Engine

### Purpose
Detect anomalies and assess situations using patterns

### Anomaly Detection

```python
def detect_anomaly(entity_id, current_context):
    """
    Detect if current behavior deviates from learned pattern
    """
    pattern = get_pattern(entity_id)
    
    # Calculate statistical deviation
    deviation = calculate_deviation(
        current=current_context,
        baseline=pattern,
        metric='mahalanobis_distance'
    )
    
    # Check against threshold
    if deviation > pattern.anomaly_threshold:
        return AnomalyAlert(
            entity_id=entity_id,
            anomaly_type=classify_anomaly(deviation),
            confidence=calculate_confidence(deviation),
            severity=assess_severity(deviation, pattern)
        )
    
    return None

def classify_anomaly(deviation):
    """
    Classify type of anomaly detected
    """
    if deviation.temporal_component > threshold:
        return 'TEMPORAL_ANOMALY'  # unusual time pattern
    elif deviation.spatial_component > threshold:
        return 'SPATIAL_ANOMALY'  # unusual location
    elif deviation.duration_component > threshold:
        return 'DURATION_ANOMALY'  # activity too long/short
    else:
        return 'GENERAL_ANOMALY'
```

### Situation Assessment

```python
def assess_situation(entity_id, current_context, anomaly=None):
    """
    Determine appropriate robot response
    """
    pattern = get_pattern(entity_id)
    
    assessment = {
        'urgency': calculate_urgency(anomaly, pattern),
        'intervention_type': determine_intervention(anomaly, pattern),
        'confidence': calculate_confidence(current_context, pattern),
        'explanation_needed': should_explain(anomaly)
    }
    
    return assessment
```

---

## 6. Action & Explanation Module

### Purpose
Execute robot behaviors and provide transparent explanations

### Action Selection

```python
def select_action(entity_id, situation_assessment):
    """
    Choose appropriate robot action based on situation
    """
    policy = get_learned_policy(entity_id)
    
    # Get action from policy
    action = policy.get_action(
        state=situation_assessment,
        exploration_rate=EPSILON
    )
    
    return action

class Action:
    """
    Represents a robot action
    """
    TYPES = [
        'APPROACH_AND_ASK',
        'NOTIFY_EMERGENCY',
        'OFFER_ASSISTANCE',
        'STAY_SILENT',
        'PROVIDE_REMINDER'
    ]
```

### Explanation Generation

```python
def generate_explanation(action, situation_assessment):
    """
    Generate pattern-based explanation
    """
    if action.type == 'APPROACH_AND_ASK':
        return "Your current activity pattern differs from " \
               "your typical pattern at this time."
    
    elif action.type == 'OFFER_ASSISTANCE':
        return "You usually appreciate assistance in this context."
    
    # NOT: "You've been sitting for 37 minutes based on 
    #       pressure sensor readings at (x,y)"
    
    return generate_abstract_explanation(situation_assessment)
```

### Learning from Feedback

```python
def learn_from_feedback(entity_id, action, outcome):
    """
    Update policy based on user feedback
    """
    policy = get_learned_policy(entity_id)
    
    # Calculate reward from outcome
    reward = calculate_reward(outcome)
    
    # Immediate policy update (online learning)
    policy.update(
        state=situation_assessment,
        action=action,
        reward=reward,
        learning_rate=LEARNING_RATE
    )
    
    save_policy(entity_id, policy)
    
    # NO storage of (state, action, reward) tuple
    # Policy updated directly, episode discarded

def calculate_reward(outcome):
    """
    Convert user feedback to reward signal
    """
    if outcome.type == 'ACCEPTED':
        return +1.0
    elif outcome.type == 'DECLINED':
        return -0.5
    elif outcome.type == 'CORRECTED':
        return -1.0
    else:
        return 0.0
```

---

## Data Flow Example: Fall Detection

```
1. SENSOR LAYER
   Pressure sensors detect unusual pattern
   ↓
   
2. FEATURE EXTRACTION
   Raw: [sensor_grid with pressure values]
   Feature: "sudden_impact + no_movement_after"
   → Discard raw data
   ↓
   
3. EPHEMERAL IDENTITY
   Match to Entity_A through spatial location + time
   ↓
   
4. PATTERN MEMORY
   Retrieve Entity_A patterns:
   - Usually active 07:00-22:00
   - Movement every 5-10 minutes typical
   - Current: No movement for 15 minutes after impact
   ↓
   
5. CONTEXT UNDERSTANDING
   ANOMALY DETECTED:
   - Type: DURATION_ANOMALY + sudden_impact
   - Deviation: 3.5σ from normal
   - Classification: Potential fall
   - Urgency: HIGH
   - Confidence: 0.87
   ↓
   
6. ACTION & EXPLANATION
   Action: APPROACH_AND_ASK
   Speech: "Are you okay?"
   
   If no response after 30 seconds:
   Action: NOTIFY_EMERGENCY
   
   Explanation (if queried):
   "I detected an unusual activity pattern and wanted 
    to check if you need assistance."
```

---

## Privacy Guarantees

### What Cannot Be Reconstructed
1. ❌ Individual's real identity or name
2. ❌ Specific events with timestamps
3. ❌ Detailed sensor readings
4. ❌ Biometric information
5. ❌ Exact movement trajectories
6. ❌ Private conversations or activities

### What Is Preserved
1. ✅ Behavioral continuity across sessions
2. ✅ Pattern-based understanding of routines
3. ✅ Anomaly detection capability
4. ✅ Contextual assistance provision
5. ✅ Learning and adaptation over time
6. ✅ Explainability of decisions

---

## Implementation Considerations

### Performance Requirements
- **Real-time feature extraction**: < 100ms latency
- **Pattern updates**: < 50ms per update
- **Anomaly detection**: < 200ms response time
- **Memory footprint**: O(entities), not O(events)

### Robustness
- Handle sensor failures gracefully
- Cope with behavioral drift over time
- Manage entity ID expiration smoothly
- Recover from power loss without data loss

### Security
- Encrypt pattern memory at rest
- Secure communication channels
- Audit logging for system behavior (not user surveillance)
- Regular security audits

---

## Testing Privacy Properties

### Unit Tests

```python
def test_no_biometric_storage():
    """Verify no facial embeddings or voiceprints stored"""
    storage = get_storage_system()
    assert not storage.contains_biometric_data()
    assert not storage.contains_image_data()
    assert not storage.contains_audio_recordings()

def test_no_event_logs():
    """Verify no timestamped event records"""
    storage = get_storage_system()
    assert not storage.contains_event_logs()
    assert not storage.contains_timestamped_actions()

def test_ephemeral_ids():
    """Verify IDs expire and cannot be reverse-engineered"""
    entity_id = create_entity_id()
    
    # Should not be linkable to real identity
    assert not can_deanonymize(entity_id)
    
    # Should expire after inactivity
    simulate_inactivity(EXPIRY_PERIOD + timedelta(days=1))
    assert not storage.exists(entity_id)

def test_pattern_abstraction():
    """Verify patterns are abstract, not concrete events"""
    entity_id = create_test_entity()
    
    # Simulate many events
    for i in range(100):
        observe_event(entity_id, generate_test_event())
    
    pattern = get_pattern(entity_id)
    
    # Should have abstract summary, not 100 events
    assert len(pattern.event_log) == 0
    assert pattern.temporal_patterns is not None
    assert pattern.spatial_patterns is not None
```

### Integration Tests

```python
def test_end_to_end_privacy():
    """Test complete flow maintains privacy"""
    # Simulate robot operation for 1 week
    simulate_operation(days=7)
    
    # Verify no sensitive data accumulated
    storage = get_storage_system()
    assert storage.total_size() < MAX_PATTERN_SIZE_PER_ENTITY * num_entities
    assert not can_reconstruct_events(storage)
    assert not can_identify_individuals(storage)
```

---

## Contact

For architecture questions or contributions:
- **Email**: harapan.bontang@gmail.com
- **GitHub Issues**: [Report technical issues](https://github.com/Wanbogang/privacy-preserving-robotics/issues)
