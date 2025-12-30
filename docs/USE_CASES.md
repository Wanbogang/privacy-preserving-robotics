# Use Cases

Detailed scenarios demonstrating the Privacy-Preserving Robotics Framework in action.

---

## 1. Eldercare Fall Detection

### Context
Elderly person (75 years old) living independently with robot assistant monitoring for safety concerns.

### Traditional Approach Problems
- 24/7 camera surveillance feels invasive and undignified
- Stored video footage creates privacy and security risks
- Family members might access recordings inappropriately
- Person feels constantly watched in their own home
- Potential for misuse in disputes or legal situations

### Privacy-Preserving Approach

**Hardware Setup:**
- Pressure sensors embedded in floor
- Thermal sensors for presence detection (no cameras)
- Audio amplitude detection (no speech recording)
- LiDAR for spatial awareness

**Week 1-2: Learning Phase**

```
Robot begins observing behavioral patterns:

Entity Detected: entity_a8f3d9e2...
- Active periods: 07:00-09:00, 12:00-14:00, 18:00-22:00
- Movement frequency: Every 15-30 minutes when active
- Typical sitting duration: 10-20 minutes
- Common zones: Kitchen (morning), Living room (afternoon/evening)
- Sleep pattern: 22:00-07:00
```

**Week 3: Normal Day**

```
08:30 - Entity active in kitchen (matches pattern)
08:45 - Entity moves to living room (normal)
09:00 - Entity sitting (within typical range)
09:18 - Entity stands, moves to bathroom (normal)
09:25 - Entity returns to living room (normal)
```

Robot remains silent - everything matches learned patterns.

**Week 3: Intervention Scenario**

```
14:15 - Sudden pressure spike detected (impact)
14:15 - No movement for 2 minutes (unusual)
14:17 - Robot approaches: "Are you okay?"
        (Audio prompt, no visual inspection)
14:17 - No verbal response detected
14:17 - No movement detected
14:18 - Robot: "I'm going to call for help"
14:18 - Emergency contact notified:
        "Unusual activity pattern detected. Wellness check recommended."
```

**Week 4: False Positive Learning**

```
16:30 - No movement for 25 minutes (approaching unusual threshold)
16:30 - Robot approaches: "Just checking - is everything okay?"
Entity: "Yes, I'm reading"
        → Robot learns: Extended sitting acceptable in afternoon + 
                        Entity usually reads 16:00-17:00
                        Update pattern: sitting_threshold[afternoon] = 35 minutes
```

### Privacy Preserved

**What Robot Knows:**
- ✅ "This entity usually active at certain times"
- ✅ "Current behavior deviates from typical pattern"
- ✅ "Extended inactivity after impact event"

**What Robot Does NOT Know:**
- ❌ Person's name, face, or identity
- ❌ What person was doing (no video)
- ❌ Specific events ("at 14:15:23 on Dec 25...")
- ❌ Ability to reconstruct past activities

**Benefits:**
- Fall detected within 3 minutes
- Help summoned without visual surveillance
- No footage for others to review
- Person maintains dignity even during vulnerable moment
- False positive rate: ~5% after 1 month learning

---

## 2. Disability Assistance

### Context
Person with mobility impairment uses wheelchair, needs occasional assistance with reaching objects and daily tasks.

### Traditional Approach Problems
- Voice assistants record all conversations (privacy breach)
- Activity logs reveal detailed health information
- Continuous monitoring creates loss of independence feeling
- Data could be accessed by insurance, family conflicts, or bad actors
- Assistance becomes surveillance

### Privacy-Preserving Approach

**Hardware Setup:**
- LiDAR for spatial awareness and positioning
- Depth camera (no RGB) for gesture recognition
- Audio keyword detection only ("help", "assist" - no full recording)
- Pressure sensors for wheelchair detection

**Week 1: Initial Learning**

```
Entity Detected: entity_c2f8a1b9... 
Profile characteristics:
- Movement pattern: Wheelchair mobility signature
- Speed: 0.5-1.2 m/s (typical wheelchair speed)
- Height profile: Lower than standing person
- Common assistance requests: High storage areas

Daily pattern:
07:30 - Entity in bathroom (30-45 min)
08:00 - Entity to kitchen
08:15 - Assistance request: "Help with coffee"
        Robot assists with reaching high shelf
        → Learning: Morning kitchen assistance typical
```

**Week 4: Proactive Assistance**

```
Morning Routine:
07:45 - Entity enters kitchen
07:46 - Robot: Positions near high cabinets (proactive, non-intrusive)
07:50 - Entity: "Thanks, I need the cereal"
        Robot: Already nearby, quick assistance
        Outcome: Positive (+1 reward)
        → Reinforce morning kitchen positioning

Alternative scenario same day:
18:30 - Entity enters kitchen
18:31 - Robot positions nearby
18:32 - Entity: "I'm fine tonight, thanks"
        Robot: Moves away immediately
        Outcome: Declined (-0.5 reward)
        → Learning: Evening independence preferred, 
                   adjust positioning behavior
```

**Adaptive Context Learning**

```
Pattern Discovered After 2 Months:
- When caregiver present (detected via second entity):
  → Assistance acceptance rate: 15%
- When entity alone:
  → Assistance acceptance rate: 75%

Robot learns:
if (num_entities_present > 1):
    reduce_proactive_assistance()
    wait_for_explicit_request()
```

### Privacy Preserved

**What Robot Knows:**
- ✅ "This entity uses wheelchair"
- ✅ "Assistance often needed in kitchen mornings"
- ✅ "Prefers independence when caregiver present"

**What Robot Does NOT Know:**
- ❌ Person's medical condition or diagnosis
- ❌ Conversations with caregivers or family
- ❌ Specific daily routines with timestamps
- ❌ Health deterioration over time (only current patterns)

**Benefits:**
- Assistance provided while preserving dignity
- No recording of private conversations
- User retains sense of control and autonomy
- Adapts to preferences without explicit programming
- Cannot be used to surveil or judge user's capabilities

---

## 3. Multi-Person Household

### Context
Family of 4: two adults (parents), two children (ages 8 and 14). Shared robot assistant for household tasks and reminders.

### Traditional Approach Problems
- Facial recognition database of entire family (security risk)
- Children's activities logged and accessible (privacy from parents)
- Data could be used in family disputes or custody situations
- Privacy violations between family members
- Risk of parental surveillance of children

### Privacy-Preserving Approach

**Hardware Setup:**
- Depth cameras (no facial recognition)
- LiDAR for presence and movement
- Audio for voice commands (no recording)
- Behavioral pattern recognition

**Week 1-2: Household Discovery**

```
Robot detects 4 distinct behavioral patterns:

Entity_A: entity_9a7f3d1e...
- Movement pattern: Adult (height ~175cm, stride ~75cm)
- Active periods: 06:00-08:00, 18:00-23:00
- Interaction style: Task-oriented, prefers brief responses
- Common zones: Kitchen (morning), Home office, Living room

Entity_B: entity_5c2b8f4a...
- Movement pattern: Adult (height ~165cm, stride ~70cm)
- Active periods: 08:00-10:00, 16:00-22:00
- Interaction style: Conversational, appreciates details
- Common zones: Kitchen, Bedroom, Living room

Entity_C: entity_7d4e1a9f...
- Movement pattern: Child (height ~130cm, higher energy)
- Active periods: 07:00-08:00 (school prep), 15:30-21:00
- Interaction style: Playful, needs reminders
- Common zones: Bedroom, Living room, Play area

Entity_D: entity_2f8c5b3d...
- Movement pattern: Teen (height ~160cm, irregular patterns)
- Active periods: Variable (typical teen schedule)
- Interaction style: Prefers independence
- Common zones: Bedroom, Kitchen (late evening)
```

**Week 4: Contextual Assistance**

**Scenario 1: Morning (Entity_A)**
```
06:30 - Entity_A detected in kitchen
06:35 - Robot: "Good morning. Weather today: Sunny, 24°C. 
                Traffic on your usual route is normal."
        (Adult-appropriate information)
07:00 - Robot: "Reminder: Team meeting at 10:00"
        (Entity_A typically appreciates schedule reminders)
07:15 - Entity_A leaves
```

**Scenario 2: After School (Entity_C)**
```
15:30 - Entity_C arrives home
15:32 - Robot: "Welcome back! Reminder: homework before screen time"
        (Age-appropriate reminder for child pattern)
15:35 - Entity_C: "What homework?"
        Robot: "Your math and reading assignments"
        (Retrieved from school calendar, not surveillance)
16:30 - Entity_C: "I finished!"
        Robot: "Great! Your favorite show starts in 15 minutes"
```

**Scenario 3: Privacy Protection**
```
Parent (Entity_A): "What has Entity_C been doing today?"
Robot: "I don't store activity logs or surveillance data. 
        I only maintain behavioral patterns to provide 
        appropriate assistance. For privacy reasons, I cannot 
        report on household members' specific activities."

Alternative appropriate query:
Parent (Entity_A): "Did Entity_C come home from school?"
Robot: "Entity matching child pattern arrived at 15:30, 
        which matches typical schedule."
```

**Scenario 4: Teen Privacy (Entity_D)**
```
23:00 - Entity_D in kitchen (late night snack - typical pattern)
23:05 - Robot remains silent (learned: Entity_D prefers no interaction)

Parent (Entity_B) next morning: "Was Entity_D up late last night?"
Robot: "I maintain patterns for assistance, not surveillance. 
        I cannot provide activity reports on household members."
```

### Privacy Preserved

**What Robot Knows:**
- ✅ "Four distinct entities with different behavioral patterns"
- ✅ "Entity patterns: adult vs child, morning vs evening preferences"
- ✅ "Interaction preferences for each entity"

**What Robot Does NOT Know:**
- ❌ Names, faces, or relationships
- ❌ Specific activities with timestamps
- ❌ Conversations or private interactions
- ❌ Reportable surveillance data

**Benefits:**
- Age-appropriate assistance for each family member
- Children's privacy protected even from parents
- No surveillance data for family disputes
- Cannot be used as monitoring tool
- Each person gets contextual help without feeling watched

**Critical Feature:**
Robot cannot be used by parents to surveil children, or by any family member to monitor others. Privacy is structural, not just policy-based.

---

## 4. Sleep Monitoring (Eldercare)

### Context
Monitoring sleep patterns to detect potential health issues without bedroom surveillance.

### Traditional Approach Problems
- Bedroom cameras extremely invasive
- Sleep data highly sensitive (proxy for health conditions)
- Video footage especially vulnerable and embarrassing
- Continuous bedroom monitoring feels uncomfortable

### Privacy-Preserving Approach

**Hardware Setup:**
- Pressure sensors (mattress/floor)
- Thermal presence detection
- Audio amplitude (distress sounds only)
- NO cameras, NO audio recording

**Week 1-4: Baseline Establishment**

```
Sleep patterns detected (statistical summary, no specific dates):

Entity: entity_4b9f2a1c...
Temporal patterns:
- Typical bedtime: 22:00-23:00 (mean: 22:30, std: 0.5hr)
- Typical wake time: 06:30-07:30 (mean: 07:00, std: 0.5hr)
- Sleep duration: 7.5-8.5 hours
- Night movements: 1-2 bathroom visits (typical)
- Movement frequency: 2-4 position changes per night
- Restlessness baseline: low variance
```

**Week 5: Normal Night**

```
Pattern Match:
22:45 - Entity enters bedroom zone (within typical range)
22:50 - Pressure indicates lying down
23:00 - Movement decreases (sleep inferred)
03:15 - Brief movement, pressure release (bathroom visit - normal pattern)
03:22 - Return to bed, pressure normalized
07:00 - Sustained movement increase (wake up)
07:15 - Entity leaves bedroom

Status: All patterns within normal variance
Action: None required
```

**Week 6: Concerning Pattern Detected**

```
Pattern Deviation:
22:30 - Entity enters bedroom (normal)
22:40 - Pressure indicates lying down (normal)
23:00 - Frequent position changes (unusual restlessness: 3σ above baseline)
01:30 - Entity gets up (much earlier than typical bathroom visit pattern)
01:45 - Still moving around (unusual duration: 15 minutes)
        Typical bathroom visit: 3-5 minutes

Robot Assessment:
- Deviation detected: Sleep disruption pattern
- Severity: Moderate (not emergency)
- Confidence: 0.78

02:00 - Robot: Gentle audio prompt "Is everything okay?"
Entity: "Can't sleep. I'm fine"

Robot Learning:
- Notes sleep disruption pattern
- Does NOT log specific events
- Updates sleep quality trend (decreasing)
- Will monitor for pattern persistence

Next Morning:
07:30 - Robot to Entity: "You seemed to have difficulty sleeping. 
        This has happened 3 times this week. Would you like me 
        to suggest relaxation techniques, or mention this to 
        your caregiver?"
```

**Week 8: Health Alert**

```
Pattern: Persistent sleep disruption for 2 weeks
- Average sleep onset delay: increased by 45 minutes
- Night restlessness: increased 3x above baseline
- Wake episodes: increased from 1-2 to 3-5 per night

Robot Assessment:
- Significant sustained deviation from baseline
- Potential health concern (not emergency)
- Recommendation: Caregiver notification

Robot to Caregiver:
"Sleep pattern analysis shows sustained changes over past 2 weeks:
- Difficulty falling asleep (delayed onset)
- Increased nighttime restlessness
- More frequent wake episodes

This may indicate discomfort, anxiety, or health changes. 
Recommend wellness check with healthcare provider.

Note: This assessment is based on pattern analysis, not 
      surveillance recordings. Specific events are not logged."
```

### Privacy Preserved

**What Robot Knows:**
- ✅ "Sleep onset typically around 23:00"
- ✅ "Restlessness has increased (statistical trend)"
- ✅ "Current sleep quality deviating from baseline"

**What Robot Does NOT Know:**
- ❌ What person was doing during restless periods
- ❌ Specific nights' detailed activities
- ❌ Visual information about person in bedroom
- ❌ Conversations or sounds (beyond distress detection)

**Benefits:**
- Sleep health monitoring without bedroom cameras
- Detects concerning patterns for early intervention
- Privacy maintained during vulnerable sleeping state
- Cannot reconstruct specific night's activities
- Health insights without creating surveillance data

---

## 5. Medication Reminder

### Context
Person takes multiple daily medications. Robot provides reminders and tracks adherence patterns (not specific compliance).

### Traditional Approach Problems
- Medication schedules reveal health conditions
- Detailed adherence logs could affect insurance
- Voice reminders might be recorded
- Privacy concerns around health data

### Privacy-Preserving Approach

**Hardware Setup:**
- Presence detection for confirmation
- Audio for reminders (no recording)
- Pattern tracking (not event logging)

**Configuration:**

```
User Setup (one-time):
- Morning medications: 08:00
- Evening medications: 20:00
- As-needed medication: Headache relief

Robot stores:
- Reminder schedules (times only)
- NO medication names or dosages
- NO health condition information
```

**Daily Operation:**

**Morning Routine:**
```
08:00 - Robot: "Morning medication reminder"
08:02 - Entity approaches robot area
        → Robot infers: Likely medication taken
        → Pattern update: morning_response_time = 2 minutes
        → NO storage: "medication taken at 08:02"

Alternative scenario:
08:00 - Robot: "Morning medication reminder"
08:15 - No entity interaction detected
08:20 - Robot: "Reminder: Morning medications" (increased salience)
08:22 - Entity approaches
        → Pattern update: sometimes_needs_second_reminder = true
```

**Evening with Complication:**
```
20:00 - Robot: "Evening medication reminder"
20:45 - No interaction detected (unusual - typical response < 10 min)
21:00 - Robot: "Reminder: Evening medications" (second attempt)
21:15 - Still no interaction
        
Robot Assessment:
- Pattern deviation: No response for 75 minutes (unusual)
- Combined with: No movement detected for 60 minutes (unusual)
- Confidence: 0.65 (moderate concern)

21:15 - Robot: Increases reminder salience, approaches entity location
21:20 - Still no response

21:25 - Robot Decision: Alert emergency contact
        Message: "Extended period without response to evening 
                 routine. This is unusual for typical patterns. 
                 Wellness check recommended."
```

**Pattern Learning (NOT Compliance Tracking):**

```
What Robot Learns:
✅ "Morning reminders typically acknowledged within 5 minutes"
✅ "Evening reminders sometimes need repetition"
✅ "Weekend mornings: delayed response acceptable (sleep-in pattern)"
✅ "When Entity_B present, reminder acceptance rate different"

What Robot Does NOT Store:
❌ "Medication taken: Yes/No" for specific dates
❌ "Missed doses: 3 times this month"
❌ Compliance percentage or adherence rates
❌ Specific timestamps of medication events
```

**Privacy in Health Emergency:**

```
Scenario: Entity non-responsive for extended period

Robot to Emergency Contact:
"I've detected an unusual pattern: no response to routine 
 prompts for over 2 hours, combined with no detected movement. 
 This significantly deviates from typical behavior. 
 Immediate wellness check recommended."

Robot Does NOT Say:
"Entity missed evening medication dose and hasn't moved 
 since 19:45. Blood pressure medication was due at 20:00."
^ This reveals health information

Privacy-Preserving Alternative:
General pattern deviation without specific health details
```

### Privacy Preserved

**What Robot Knows:**
- ✅ "Reminder schedules (times)"
- ✅ "Typical response patterns"
- ✅ "Current behavior vs typical pattern"

**What Robot Does NOT Know:**
- ❌ Specific medications or health conditions
- ❌ Adherence rates or missed doses
- ❌ Health outcomes or effectiveness
- ❌ Reasons for pattern changes

**Benefits:**
- Medication reminders without health data exposure
- Detects concerning non-response patterns
- No compliance data for insurance/others to access
- Privacy maintained around sensitive health information
- Pattern-based rather than event-based tracking

---

## Common Patterns Across Use Cases

### 1. Learning Phase
All scenarios include initial learning period where robot observes patterns without intervention.

### 2. Pattern-Based Understanding
Robot understands "typical" vs "unusual" without storing specific events.

### 3. Graduated Response
Robot escalates intervention based on deviation severity:
- Minor deviation → Silent observation
- Moderate deviation → Gentle inquiry
- Significant deviation → Active intervention
- Emergency pattern → Alert contacts

### 4. User Feedback Learning
Robot adapts based on user responses (accepted, declined, corrected).

### 5. Privacy Protection from Others
Robot cannot be used by family members, caregivers, or others to surveil the primary user.

---

## Implementation Notes

### Technical Requirements
- Real-time pattern matching (< 200ms)
- Anomaly detection without event storage
- Behavioral re-identification across sessions
- Graceful handling of pattern drift

### User Experience
- Transparent about capabilities and limitations
- Allows users to query learned patterns
- Provides reset/forget mechanisms
- Clear communication about privacy protections

### Ethical Considerations
- Informed consent about pattern learning
- Right to explanation of robot decisions
- Ability to opt-out of specific features
- Regular privacy audits and reviews

---

## Contact

For use case questions, real-world implementation discussions, or to contribute additional scenarios:

**Email**: harapan.bontang@gmail.com  
**GitHub**: [privacy-preserving-robotics](https://github.com/Wanbogang/privacy-preserving-robotics)
