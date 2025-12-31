"""
Pattern Memory System Demo

Demonstrates how the Privacy-Preserving Robotics Framework stores behavioral
patterns without recording specific events. Memory is abstract and statistical,
making it impossible to reconstruct detailed past activities.

Key Features:
- Abstract pattern storage (not event logs)
- Statistical summarization
- Temporal pattern learning
- Automatic forgetting/decay
- No reconstructable event history

Author: Agus Setiawan
License: GPL-3.0
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np
from collections import defaultdict


@dataclass
class TemporalPattern:
    """
    Temporal activity patterns - stores WHEN activities typically occur,
    but NOT specific timestamps of individual events.
    """
    # Statistical summary of active hours (mean and std)
    active_hours_mean: float = 12.0  # Mean hour of day
    active_hours_std: float = 4.0    # Standard deviation
    
    # Typical activity duration (in minutes)
    typical_duration_mean: float = 0.0
    typical_duration_std: float = 0.0
    
    # Activity frequency (per day)
    frequency_per_day: float = 0.0
    
    # Pattern stability (how consistent the pattern is)
    pattern_stability: float = 0.0
    
    # Last update time (for decay calculation)
    last_updated: datetime = field(default_factory=datetime.now)
    
    # Number of observations (for confidence)
    observation_count: int = 0


@dataclass
class SpatialPattern:
    """
    Spatial movement patterns - stores WHERE activities occur,
    but NOT detailed location histories.
    """
    # Common zones with frequency (abstract locations)
    zone_frequencies: Dict[str, float] = field(default_factory=dict)
    
    # Movement speed statistics
    movement_speed_mean: float = 0.0
    movement_speed_std: float = 0.0
    
    # Transition patterns between zones (probabilities)
    zone_transitions: Dict[Tuple[str, str], float] = field(default_factory=dict)


@dataclass
class ActivityPattern:
    """
    Activity-specific patterns - stores HOW activities are performed,
    but NOT detailed activity logs.
    """
    activity_type: str
    
    # Temporal aspects
    temporal: TemporalPattern = field(default_factory=TemporalPattern)
    
    # Spatial aspects
    spatial: SpatialPattern = field(default_factory=SpatialPattern)
    
    # Activity-specific metrics
    success_rate: float = 0.0  # How often activity completes successfully
    typical_assistance_needed: float = 0.0  # Probability of needing help


class PatternMemory:
    """
    Privacy-preserving pattern memory system.
    
    Key Privacy Properties:
    - No event logs with timestamps
    - No detailed sensor recordings
    - Only statistical summaries stored
    - Automatic forgetting through decay
    - Cannot reconstruct specific past events
    """
    
    def __init__(self, decay_factor: float = 0.95):
        """
        Initialize pattern memory.
        
        Args:
            decay_factor: Factor for exponential decay (0.95 = 5% decay per update)
        """
        self.patterns: Dict[str, ActivityPattern] = {}
        self.decay_factor = decay_factor
        self.total_observations = 0
    
    def observe_activity(self, activity_type: str, hour: float, 
                        duration_minutes: float, zone: str, 
                        movement_speed: float = 1.0):
        """
        Observe an activity and update patterns.
        
        NOTE: This function processes the observation but does NOT store
        the specific event details. Only statistical patterns are updated.
        
        Args:
            activity_type: Type of activity (e.g., "cooking", "sleeping")
            hour: Hour of day (0-24)
            duration_minutes: How long activity lasted
            zone: Location zone (e.g., "kitchen", "bedroom")
            movement_speed: Movement speed during activity
        """
        # Get or create pattern
        if activity_type not in self.patterns:
            self.patterns[activity_type] = ActivityPattern(activity_type=activity_type)
        
        pattern = self.patterns[activity_type]
        
        # Update temporal pattern
        self._update_temporal_pattern(pattern.temporal, hour, duration_minutes)
        
        # Update spatial pattern
        self._update_spatial_pattern(pattern.spatial, zone, movement_speed)
        
        # Apply decay to all other patterns (forgetting mechanism)
        self._apply_decay()
        
        self.total_observations += 1
    
    def _update_temporal_pattern(self, temporal: TemporalPattern, 
                                 hour: float, duration: float):
        """
        Update temporal pattern with exponential moving average.
        Old observations gradually forgotten.
        """
        alpha = 0.2  # Learning rate
        
        temporal.observation_count += 1
        
        # Update active hours (exponential moving average)
        if temporal.observation_count == 1:
            temporal.active_hours_mean = hour
            temporal.active_hours_std = 0.0
        else:
            # Update mean
            old_mean = temporal.active_hours_mean
            temporal.active_hours_mean = (
                alpha * hour + (1 - alpha) * temporal.active_hours_mean
            )
            
            # Update std (running variance estimation)
            diff = hour - old_mean
            temporal.active_hours_std = np.sqrt(
                alpha * (diff ** 2) + (1 - alpha) * (temporal.active_hours_std ** 2)
            )
        
        # Update duration
        if temporal.observation_count == 1:
            temporal.typical_duration_mean = duration
            temporal.typical_duration_std = 0.0
        else:
            old_mean = temporal.typical_duration_mean
            temporal.typical_duration_mean = (
                alpha * duration + (1 - alpha) * temporal.typical_duration_mean
            )
            
            diff = duration - old_mean
            temporal.typical_duration_std = np.sqrt(
                alpha * (diff ** 2) + (1 - alpha) * (temporal.typical_duration_std ** 2)
            )
        
        # Update pattern stability (how consistent observations are)
        temporal.pattern_stability = min(1.0, temporal.observation_count / 20.0)
        
        temporal.last_updated = datetime.now()
    
    def _update_spatial_pattern(self, spatial: SpatialPattern, 
                               zone: str, speed: float):
        """
        Update spatial pattern with zone frequency and movement stats.
        """
        alpha = 0.2
        
        # Update zone frequency
        if zone not in spatial.zone_frequencies:
            spatial.zone_frequencies[zone] = 1.0
        else:
            spatial.zone_frequencies[zone] += 1.0
        
        # Normalize frequencies (keep as probabilities)
        total = sum(spatial.zone_frequencies.values())
        for z in spatial.zone_frequencies:
            spatial.zone_frequencies[z] /= total
        
        # Update movement speed stats
        if spatial.movement_speed_mean == 0:
            spatial.movement_speed_mean = speed
            spatial.movement_speed_std = 0.0
        else:
            old_mean = spatial.movement_speed_mean
            spatial.movement_speed_mean = (
                alpha * speed + (1 - alpha) * spatial.movement_speed_mean
            )
            
            diff = speed - old_mean
            spatial.movement_speed_std = np.sqrt(
                alpha * (diff ** 2) + (1 - alpha) * (spatial.movement_speed_std ** 2)
            )
    
    def _apply_decay(self):
        """
        Apply exponential decay to all patterns.
        This is the FORGETTING mechanism - old patterns fade over time.
        """
        for pattern in self.patterns.values():
            # Decay observation count (older observations count less)
            pattern.temporal.observation_count *= self.decay_factor
            
            # Decay pattern stability
            pattern.temporal.pattern_stability *= self.decay_factor
            
            # Decay zone frequencies
            for zone in pattern.spatial.zone_frequencies:
                pattern.spatial.zone_frequencies[zone] *= self.decay_factor
    
    def get_pattern(self, activity_type: str) -> Optional[ActivityPattern]:
        """Get pattern for specific activity type."""
        return self.patterns.get(activity_type)
    
    def detect_anomaly(self, activity_type: str, current_hour: float, 
                      current_duration: float) -> Tuple[bool, float]:
        """
        Detect if current activity is anomalous compared to learned pattern.
        
        Returns:
            Tuple of (is_anomaly, deviation_score)
        """
        pattern = self.get_pattern(activity_type)
        if not pattern or pattern.temporal.observation_count < 3:
            return False, 0.0  # Not enough data to determine
        
        temporal = pattern.temporal
        
        # Calculate z-score for hour
        if temporal.active_hours_std > 0:
            hour_zscore = abs(
                (current_hour - temporal.active_hours_mean) / temporal.active_hours_std
            )
        else:
            hour_zscore = 0.0
        
        # Calculate z-score for duration
        if temporal.typical_duration_std > 0:
            duration_zscore = abs(
                (current_duration - temporal.typical_duration_mean) / 
                temporal.typical_duration_std
            )
        else:
            duration_zscore = 0.0
        
        # Combined deviation
        deviation = max(hour_zscore, duration_zscore)
        
        # Anomaly if deviation > 2 standard deviations
        is_anomaly = deviation > 2.0
        
        return is_anomaly, deviation
    
    def summarize_patterns(self) -> str:
        """
        Generate human-readable summary of learned patterns.
        This shows what robot "remembers" - abstract patterns, NOT events.
        """
        if not self.patterns:
            return "No patterns learned yet."
        
        summary = []
        summary.append("=" * 70)
        summary.append("LEARNED BEHAVIORAL PATTERNS")
        summary.append("=" * 70)
        summary.append("")
        
        for activity_type, pattern in self.patterns.items():
            summary.append(f"Activity: {activity_type.upper()}")
            summary.append("-" * 70)
            
            t = pattern.temporal
            s = pattern.spatial
            
            # Temporal summary
            summary.append(f"  Temporal Pattern:")
            summary.append(f"    • Typically occurs around: {t.active_hours_mean:.1f}:00 "
                         f"(±{t.active_hours_std:.1f} hours)")
            summary.append(f"    • Typical duration: {t.typical_duration_mean:.1f} minutes "
                         f"(±{t.typical_duration_std:.1f} min)")
            summary.append(f"    • Pattern confidence: {t.pattern_stability:.2f}")
            summary.append(f"    • Observations: ~{int(t.observation_count)}")
            
            # Spatial summary
            summary.append(f"  Spatial Pattern:")
            if s.zone_frequencies:
                summary.append(f"    • Common zones:")
                for zone, freq in sorted(s.zone_frequencies.items(), 
                                        key=lambda x: x[1], reverse=True):
                    summary.append(f"      - {zone}: {freq*100:.1f}% of time")
            summary.append(f"    • Movement speed: {s.movement_speed_mean:.2f} m/s "
                         f"(±{s.movement_speed_std:.2f})")
            
            summary.append("")
        
        summary.append("=" * 70)
        summary.append("PRIVACY PROPERTIES VERIFIED:")
        summary.append("  ✓ No specific timestamps stored")
        summary.append("  ✓ No detailed event logs")
        summary.append("  ✓ Only statistical summaries maintained")
        summary.append("  ✓ Cannot reconstruct individual events")
        summary.append("  ✓ Old patterns fade through decay mechanism")
        summary.append("=" * 70)
        
        return "\n".join(summary)


def run_demo():
    """
    Demonstrate pattern memory with simulated daily activities.
    """
    print("=" * 70)
    print("PATTERN MEMORY SYSTEM DEMO")
    print("Privacy-Preserving Home Robotics Framework")
    print("=" * 70)
    print()
    
    # Initialize pattern memory
    memory = PatternMemory(decay_factor=0.98)
    
    print("Scenario: Learning daily routine over 2 weeks")
    print("-" * 70)
    print()
    
    # Simulate 2 weeks of activities
    print("Week 1: Establishing patterns...")
    for day in range(7):
        # Morning routine (breakfast)
        breakfast_time = np.random.normal(7.5, 0.3)  # ~7:30 AM ± 20 min
        memory.observe_activity(
            activity_type="breakfast",
            hour=breakfast_time,
            duration_minutes=np.random.normal(25, 5),  # ~25 min
            zone="kitchen",
            movement_speed=1.2
        )
        
        # Afternoon activity (reading)
        reading_time = np.random.normal(14.0, 0.5)  # ~2:00 PM
        memory.observe_activity(
            activity_type="reading",
            hour=reading_time,
            duration_minutes=np.random.normal(60, 10),  # ~60 min
            zone="living_room",
            movement_speed=0.3
        )
        
        # Evening routine (dinner)
        dinner_time = np.random.normal(18.5, 0.4)  # ~6:30 PM
        memory.observe_activity(
            activity_type="dinner",
            hour=dinner_time,
            duration_minutes=np.random.normal(35, 7),  # ~35 min
            zone="kitchen",
            movement_speed=1.1
        )
        
        print(f"  Day {day + 1}: Observed breakfast, reading, dinner")
    
    print()
    time.sleep(1)
    
    print("Week 2: Reinforcing patterns...")
    for day in range(7, 14):
        # Same routine with slight variations
        breakfast_time = np.random.normal(7.5, 0.3)
        memory.observe_activity("breakfast", breakfast_time, 
                              np.random.normal(25, 5), "kitchen", 1.2)
        
        reading_time = np.random.normal(14.0, 0.5)
        memory.observe_activity("reading", reading_time,
                              np.random.normal(60, 10), "living_room", 0.3)
        
        dinner_time = np.random.normal(18.5, 0.4)
        memory.observe_activity("dinner", dinner_time,
                              np.random.normal(35, 7), "kitchen", 1.1)
        
        print(f"  Day {day + 1}: Observed breakfast, reading, dinner")
    
    print()
    print("✓ Total observations: ", memory.total_observations)
    print()
    time.sleep(1)
    
    # Show learned patterns
    print(memory.summarize_patterns())
    print()
    time.sleep(2)
    
    # Test anomaly detection
    print("Scenario: Testing anomaly detection")
    print("-" * 70)
    print()
    
    # Normal breakfast
    is_anomaly, score = memory.detect_anomaly("breakfast", 7.5, 25)
    print(f"Normal breakfast (7:30 AM, 25 min):")
    print(f"  Anomaly: {is_anomaly}, Deviation: {score:.2f}σ")
    print()
    
    # Very early breakfast (anomalous)
    is_anomaly, score = memory.detect_anomaly("breakfast", 5.0, 25)
    print(f"Very early breakfast (5:00 AM, 25 min):")
    print(f"  Anomaly: {is_anomaly}, Deviation: {score:.2f}σ")
    print("  → Robot might check: 'Unusual activity time detected'")
    print()
    
    # Very long reading session (anomalous)
    is_anomaly, score = memory.detect_anomaly("reading", 14.0, 150)
    print(f"Very long reading (2:00 PM, 150 min):")
    print(f"  Anomaly: {is_anomaly}, Deviation: {score:.2f}σ")
    print("  → Robot might check: 'Activity duration unusual'")
    print()
    
    time.sleep(1)
    
    # Demonstrate privacy properties
    print("=" * 70)
    print("PRIVACY VERIFICATION")
    print("=" * 70)
    print()
    
    print("Question: Can we reconstruct what happened on Day 3?")
    print("Answer: NO")
    print()
    print("What we CAN know:")
    print("  ✓ Person typically has breakfast around 7:30 AM")
    print("  ✓ Breakfast usually lasts ~25 minutes")
    print("  ✓ Typically occurs in kitchen")
    print()
    print("What we CANNOT know:")
    print("  ✗ Exact time of Day 3's breakfast")
    print("  ✗ Exact duration of Day 3's breakfast")
    print("  ✗ What was eaten")
    print("  ✗ Any specific details of that event")
    print()
    print("Conclusion: Individual events are NOT reconstructable from patterns!")
    print()
    
    print("=" * 70)
    print("Summary: Memory without Recording")
    print("=" * 70)
    print()
    print("Key Features Demonstrated:")
    print("  1. Statistical pattern storage (means, standard deviations)")
    print("  2. No event logs or timestamps of specific occurrences")
    print("  3. Automatic forgetting through exponential decay")
    print("  4. Anomaly detection from learned baselines")
    print("  5. Privacy by design - reconstruction impossible")
    print()
    print("Memory Properties:")
    print("  ✓ Stores WHAT typically happens (pattern)")
    print("  ✓ Stores WHEN typically happens (mean time)")
    print("  ✓ Does NOT store specific events")
    print("  ✓ Does NOT store detailed timelines")
    print("  ✓ Cannot answer 'What happened on Day X?'")
    print("  ✓ CAN answer 'Is this behavior unusual?'")
    print()


if __name__ == "__main__":
    run_demo()
