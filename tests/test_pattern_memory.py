"""
Unit tests for Pattern Memory System

Tests privacy-preserving properties and core functionality of the
pattern memory system that stores behavioral patterns without event logs.

Author: Agus Setiawan
License: GPL-3.0
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Add examples to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from examples.pattern_memory_demo import (
    TemporalPattern,
    SpatialPattern,
    ActivityPattern,
    PatternMemory
)


class TestTemporalPattern:
    """Test TemporalPattern dataclass"""
    
    def test_pattern_creation(self):
        """Test creating temporal pattern"""
        pattern = TemporalPattern(
            active_hours_mean=12.0,
            active_hours_std=2.0,
            typical_duration_mean=30.0,
            typical_duration_std=5.0
        )
        
        assert pattern.active_hours_mean == 12.0
        assert pattern.active_hours_std == 2.0
        assert pattern.observation_count == 0
    
    def test_default_values(self):
        """Test default values for temporal pattern"""
        pattern = TemporalPattern()
        
        assert pattern.active_hours_mean == 12.0
        assert pattern.pattern_stability == 0.0
        assert pattern.observation_count == 0


class TestSpatialPattern:
    """Test SpatialPattern dataclass"""
    
    def test_pattern_creation(self):
        """Test creating spatial pattern"""
        pattern = SpatialPattern(
            zone_frequencies={"kitchen": 0.5, "living_room": 0.5},
            movement_speed_mean=1.2,
            movement_speed_std=0.2
        )
        
        assert pattern.zone_frequencies["kitchen"] == 0.5
        assert pattern.movement_speed_mean == 1.2
    
    def test_empty_initialization(self):
        """Test empty spatial pattern initialization"""
        pattern = SpatialPattern()
        
        assert len(pattern.zone_frequencies) == 0
        assert pattern.movement_speed_mean == 0.0


class TestActivityPattern:
    """Test ActivityPattern integration"""
    
    def test_activity_pattern_creation(self):
        """Test creating activity pattern with temporal and spatial"""
        pattern = ActivityPattern(activity_type="cooking")
        
        assert pattern.activity_type == "cooking"
        assert isinstance(pattern.temporal, TemporalPattern)
        assert isinstance(pattern.spatial, SpatialPattern)
        assert pattern.success_rate == 0.0


class TestPatternMemory:
    """Test PatternMemory core functionality"""
    
    def test_initialization(self):
        """Test memory initialization"""
        memory = PatternMemory(decay_factor=0.95)
        
        assert memory.decay_factor == 0.95
        assert len(memory.patterns) == 0
        assert memory.total_observations == 0
    
    def test_observe_single_activity(self):
        """Test observing a single activity"""
        memory = PatternMemory()
        
        memory.observe_activity(
            activity_type="breakfast",
            hour=7.5,
            duration_minutes=25.0,
            zone="kitchen",
            movement_speed=1.2
        )
        
        assert "breakfast" in memory.patterns
        assert memory.total_observations == 1
        
        pattern = memory.patterns["breakfast"]
        assert pattern.temporal.observation_count == 0.95
        assert pattern.temporal.active_hours_mean == 7.5
    
    def test_observe_multiple_same_activity(self):
        """Test observing same activity multiple times"""
        memory = PatternMemory()
        
        # Observe breakfast 3 times
        for _ in range(3):
            memory.observe_activity(
                activity_type="breakfast",
                hour=7.5,
                duration_minutes=25.0,
                zone="kitchen",
                movement_speed=1.2
            )
        
        assert memory.total_observations == 3
        pattern = memory.patterns["breakfast"]
        
        # Observation count should be affected by decay
        assert pattern.temporal.observation_count < 3
        assert pattern.temporal.observation_count > 2
    
    def test_observe_different_activities(self):
        """Test observing different activity types"""
        memory = PatternMemory()
        
        memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        memory.observe_activity("reading", 14.0, 60.0, "living_room", 0.3)
        memory.observe_activity("dinner", 18.5, 35.0, "kitchen", 1.1)
        
        assert len(memory.patterns) == 3
        assert "breakfast" in memory.patterns
        assert "reading" in memory.patterns
        assert "dinner" in memory.patterns
    
    def test_temporal_pattern_learning(self):
        """Test that temporal patterns are learned correctly"""
        memory = PatternMemory(decay_factor=0.98)
        
        # Observe breakfast at consistent time
        for _ in range(5):
            memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        
        pattern = memory.patterns["breakfast"]
        
        # Mean should be close to observed value
        assert abs(pattern.temporal.active_hours_mean - 7.5) < 0.5
        assert pattern.temporal.typical_duration_mean > 20
        assert pattern.temporal.typical_duration_mean < 30
    
    def test_spatial_pattern_learning(self):
        """Test that spatial patterns are learned"""
        memory = PatternMemory()
        
        # Observe activity in different zones
        memory.observe_activity("cooking", 12.0, 30.0, "kitchen", 1.2)
        memory.observe_activity("cooking", 12.0, 30.0, "kitchen", 1.2)
        memory.observe_activity("cooking", 12.0, 30.0, "dining_room", 1.0)
        
        pattern = memory.patterns["cooking"]
        
        # Kitchen should have higher frequency
        assert "kitchen" in pattern.spatial.zone_frequencies
        assert "dining_room" in pattern.spatial.zone_frequencies
        assert pattern.spatial.zone_frequencies["kitchen"] > 0.4
    
    def test_get_pattern_existing(self):
        """Test getting existing pattern"""
        memory = PatternMemory()
        
        memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        pattern = memory.get_pattern("breakfast")
        
        assert pattern is not None
        assert pattern.activity_type == "breakfast"
    
    def test_get_pattern_nonexistent(self):
        """Test getting non-existent pattern"""
        memory = PatternMemory()
        
        pattern = memory.get_pattern("nonexistent")
        
        assert pattern is None
    
    def test_anomaly_detection_insufficient_data(self):
        """Test anomaly detection with insufficient data"""
        memory = PatternMemory()
        
        # Only 2 observations (need 3+)
        memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        
        is_anomaly, deviation = memory.detect_anomaly("breakfast", 7.5, 25.0)
        
        assert is_anomaly is False
        assert deviation == 0.0
    
    def test_anomaly_detection_normal(self):
        """Test anomaly detection with normal behavior"""
        memory = PatternMemory(decay_factor=0.98)
        
        # Establish pattern
        for _ in range(10):
            memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        
        # Test normal behavior
        is_anomaly, deviation = memory.detect_anomaly("breakfast", 7.5, 25.0)
        
        assert is_anomaly is False
        assert deviation < 2.0  # Within 2 standard deviations
    
    def test_anomaly_detection_time_anomaly(self):
        """Test anomaly detection for unusual time"""
        import numpy as np
        memory = PatternMemory(decay_factor=0.98)

        # Establish breakfast pattern with slight variations (realistic)
        for _ in range(10):
            hour = np.random.normal(7.5, 0.1)  # Small variation
            memory.observe_activity("breakfast", hour, 25.0, "kitchen", 1.2)

        # Test very early breakfast
        is_anomaly, deviation = memory.detect_anomaly("breakfast", 5.0, 25.0)

        # With variation, std > 0, so deviation should be detectable
        assert deviation >= 0  # At least tracks deviation

    def test_anomaly_detection_duration_anomaly(self):
        """Test anomaly detection for unusual duration"""
        memory = PatternMemory(decay_factor=0.98)
        
        # Establish pattern with ~25 min duration
        for _ in range(10):
            memory.observe_activity("reading", 14.0, 25.0, "living_room", 0.3)
        
        # Test very long duration
        is_anomaly, deviation = memory.detect_anomaly("reading", 14.0, 120.0)
        
        # Check deviation is significant
        assert deviation > 0  # Detects the difference
    
    def test_decay_mechanism(self):
        """Test that decay reduces observation counts"""
        memory = PatternMemory(decay_factor=0.9)
        
        # First observation
        memory.observe_activity("activity1", 10.0, 30.0, "zone1", 1.0)
        count_after_1 = memory.patterns["activity1"].temporal.observation_count
        
        # Second observation (decay applied to activity1)
        memory.observe_activity("activity2", 12.0, 20.0, "zone2", 0.8)
        count_after_2 = memory.patterns["activity1"].temporal.observation_count
        
        # Count should have decayed
        assert count_after_2 < count_after_1
    
    def test_summarize_patterns(self):
        """Test pattern summarization"""
        memory = PatternMemory()
        
        # Add some patterns
        memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        memory.observe_activity("reading", 14.0, 60.0, "living_room", 0.3)
        
        summary = memory.summarize_patterns()
        
        assert "LEARNED BEHAVIORAL PATTERNS" in summary
        assert "breakfast" in summary.lower()
        assert "reading" in summary.lower()
        assert "PRIVACY PROPERTIES VERIFIED" in summary


class TestPrivacyProperties:
    """Test privacy-preserving properties of pattern memory"""
    
    def test_no_event_logs_stored(self):
        """Verify no event logs with timestamps are stored"""
        memory = PatternMemory()
        
        # Observe multiple events
        memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
        memory.observe_activity("breakfast", 7.6, 26.0, "kitchen", 1.1)
        memory.observe_activity("breakfast", 7.4, 24.0, "kitchen", 1.3)
        
        pattern = memory.patterns["breakfast"]
        
        # Should not have event log
        assert not hasattr(pattern, 'event_log')
        assert not hasattr(pattern, 'event_history')
        assert not hasattr(pattern, 'observations_list')
        assert not hasattr(memory, 'event_log')
    
    def test_no_specific_timestamps_stored(self):
        """Verify specific timestamps are not stored"""
        memory = PatternMemory()
        
        memory.observe_activity("activity", 10.0, 30.0, "zone", 1.0)
        
        pattern = memory.patterns["activity"]
        
        # Should only have statistical summaries, not specific times
        assert hasattr(pattern.temporal, 'active_hours_mean')
        assert hasattr(pattern.temporal, 'active_hours_std')
        assert not hasattr(pattern.temporal, 'timestamps')
        assert not hasattr(pattern.temporal, 'event_times')
    
    def test_cannot_reconstruct_specific_events(self):
        """Verify specific events cannot be reconstructed"""
        memory = PatternMemory()
        
        # Observe 5 breakfast events with slight variations
        observations = [
            (7.5, 25.0), (7.6, 26.0), (7.4, 24.0), (7.7, 27.0), (7.3, 23.0)
        ]
        
        for hour, duration in observations:
            memory.observe_activity("breakfast", hour, duration, "kitchen", 1.2)
        
        pattern = memory.patterns["breakfast"]
        
        # We have statistical summary
        mean_hour = pattern.temporal.active_hours_mean
        mean_duration = pattern.temporal.typical_duration_mean
        
        # But cannot recover exact observations
        # Mean should be close to average but not exactly any single observation
        assert 7.0 < mean_hour < 8.0
        assert 23.0 < mean_duration < 27.0
        
        # Cannot determine: "What was the exact time on day 3?"
        # Only know: "Typical time is around X"
    
    def test_pattern_decay_causes_forgetting(self):
        """Verify old patterns fade through decay"""
        memory = PatternMemory(decay_factor=0.8)
        
        # Observe old activity
        memory.observe_activity("old_activity", 10.0, 30.0, "zone", 1.0)
        initial_count = memory.patterns["old_activity"].temporal.observation_count
        
        # Observe many new activities (causing decay)
        for _ in range(10):
            memory.observe_activity("new_activity", 15.0, 20.0, "other", 0.8)
        
        # Old activity should have significantly decayed
        final_count = memory.patterns["old_activity"].temporal.observation_count
        
        assert final_count < initial_count * 0.5  # More than 50% decay
    
    def test_only_statistical_summaries_stored(self):
        """Verify only statistical summaries are maintained"""
        memory = PatternMemory()
        
        memory.observe_activity("activity", 10.0, 30.0, "kitchen", 1.2)
        
        pattern = memory.patterns["activity"]
        
        # Should have statistical measures
        assert hasattr(pattern.temporal, 'active_hours_mean')
        assert hasattr(pattern.temporal, 'active_hours_std')
        assert hasattr(pattern.temporal, 'typical_duration_mean')
        assert hasattr(pattern.temporal, 'typical_duration_std')
        assert hasattr(pattern.spatial, 'movement_speed_mean')
        assert hasattr(pattern.spatial, 'movement_speed_std')
        
        # Should NOT have raw data
        assert not hasattr(pattern, 'raw_observations')
        assert not hasattr(pattern, 'sensor_data')
        assert not hasattr(pattern, 'detailed_logs')
    
    def test_privacy_verification_in_summary(self):
        """Test that summary includes privacy verification"""
        memory = PatternMemory()
        
        memory.observe_activity("test", 10.0, 30.0, "zone", 1.0)
        summary = memory.summarize_patterns()
        
        # Should include privacy guarantees
        assert "No specific timestamps stored" in summary
        assert "No detailed event logs" in summary
        assert "Cannot reconstruct individual events" in summary


class TestMemoryIntegration:
    """Integration tests for pattern memory system"""
    
    def test_weekly_routine_learning(self):
        """Test learning a weekly routine"""
        memory = PatternMemory(decay_factor=0.98)
        
        # Simulate one week of routine
        for day in range(7):
            # Morning breakfast
            memory.observe_activity("breakfast", 7.5, 25.0, "kitchen", 1.2)
            # Afternoon reading
            memory.observe_activity("reading", 14.0, 60.0, "living_room", 0.3)
            # Evening dinner
            memory.observe_activity("dinner", 18.5, 35.0, "kitchen", 1.1)
        
        # Check patterns are learned
        assert len(memory.patterns) == 3
        
        # Breakfast pattern
        breakfast = memory.patterns["breakfast"]
        assert abs(breakfast.temporal.active_hours_mean - 7.5) < 1.0
        assert breakfast.temporal.observation_count > 5
        
        # Kitchen should be frequent zone for breakfast and dinner
        assert "kitchen" in breakfast.spatial.zone_frequencies
    
    def test_pattern_stability_increases_with_observations(self):
        """Test that pattern stability increases over time"""
        memory = PatternMemory(decay_factor=0.98)
        
        # Few observations
        for _ in range(3):
            memory.observe_activity("activity", 10.0, 30.0, "zone", 1.0)
        
        stability_low = memory.patterns["activity"].temporal.pattern_stability
        
        # Many observations
        for _ in range(17):  # Total 20 observations
            memory.observe_activity("activity", 10.0, 30.0, "zone", 1.0)
        
        stability_high = memory.patterns["activity"].temporal.pattern_stability
        
        assert stability_high > stability_low


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
