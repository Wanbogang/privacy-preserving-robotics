"""
Unit tests for Ephemeral Identity Management

Tests privacy-preserving properties and core functionality of the
ephemeral identity system.

Author: Agus Setiawan
License: GPL-3.0
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Add examples to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from examples.ephemeral_identity_demo import (
    BehavioralFeatures,
    EntityProfile,
    EphemeralIdentityManager
)


class TestBehavioralFeatures:
    """Test BehavioralFeatures dataclass"""
    
    def test_feature_creation(self):
        """Test creating behavioral features"""
        features = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        assert features.movement_speed == 1.2
        assert features.height_estimate == 1.75
        assert features.activity_time == "morning"
    
    def test_to_vector(self):
        """Test converting features to numerical vector"""
        features = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        vector = features.to_vector()
        
        assert len(vector) == 5
        assert vector[0] == 1.2  # movement_speed
        assert vector[1] == 1.75  # height_estimate
        assert vector[2] == 0  # morning encoded as 0
        assert vector[3] == 0  # kitchen encoded as 0
        assert vector[4] == 0  # steady encoded as 0


class TestEntityProfile:
    """Test EntityProfile functionality"""
    
    def test_profile_creation(self):
        """Test creating entity profile"""
        now = datetime.now()
        profile = EntityProfile(
            entity_id="test_entity_123",
            first_observed=now,
            last_seen=now,
            observation_count=1,
            confidence=0.1
        )
        
        assert profile.entity_id == "test_entity_123"
        assert profile.observation_count == 1
        assert profile.confidence == 0.1
    
    def test_is_expired_not_expired(self):
        """Test entity is not expired when recently seen"""
        now = datetime.now()
        profile = EntityProfile(
            entity_id="test_123",
            first_observed=now,
            last_seen=now,
            observation_count=1
        )
        
        assert not profile.is_expired(expiry_days=30)
    
    def test_is_expired_expired(self):
        """Test entity is expired after inactivity"""
        now = datetime.now()
        old_time = now - timedelta(days=35)
        
        profile = EntityProfile(
            entity_id="test_123",
            first_observed=old_time,
            last_seen=old_time,
            observation_count=1
        )
        
        assert profile.is_expired(expiry_days=30)
    
    def test_update_increases_confidence(self):
        """Test that updates increase confidence"""
        features = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        profile = EntityProfile(
            entity_id="test_123",
            first_observed=datetime.now(),
            last_seen=datetime.now(),
            observation_count=0,
            confidence=0.0
        )
        
        initial_confidence = profile.confidence
        profile.update(features)
        
        assert profile.confidence > initial_confidence
        assert profile.observation_count == 1


class TestEphemeralIdentityManager:
    """Test EphemeralIdentityManager core functionality"""
    
    def test_initialization(self):
        """Test manager initialization"""
        manager = EphemeralIdentityManager(
            similarity_threshold=0.85,
            expiry_days=30
        )
        
        assert manager.similarity_threshold == 0.85
        assert manager.expiry_days == 30
        assert len(manager.entities) == 0
    
    def test_generate_entity_id_format(self):
        """Test entity ID generation format"""
        manager = EphemeralIdentityManager()
        entity_id = manager.generate_entity_id()
        
        assert entity_id.startswith("entity_")
        assert len(entity_id) > 10  # Should be long random string
    
    def test_generate_entity_id_uniqueness(self):
        """Test that generated IDs are unique"""
        manager = EphemeralIdentityManager()
        
        ids = [manager.generate_entity_id() for _ in range(100)]
        
        assert len(ids) == len(set(ids))  # All unique
    
    def test_calculate_similarity_identical(self):
        """Test similarity calculation for identical features"""
        manager = EphemeralIdentityManager()
        
        features = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        similarity = manager.calculate_similarity(features, features)
        
        assert similarity == 1.0  # Identical should be 1.0
    
    def test_calculate_similarity_very_different(self):
        """Test similarity for very different features"""
        manager = EphemeralIdentityManager()
        
        features1 = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        features2 = BehavioralFeatures(
            movement_speed=0.5,  # Much slower
            height_estimate=1.50,  # Much shorter
            activity_time="evening",
            interaction_zone="bedroom",
            movement_pattern="variable"
        )
        
        similarity = manager.calculate_similarity(features1, features2)
        
        assert similarity < 0.75  # Very different should be low
    
    def test_calculate_similarity_similar(self):
        """Test similarity for similar features"""
        manager = EphemeralIdentityManager()
        
        features1 = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        features2 = BehavioralFeatures(
            movement_speed=1.15,  # Slightly different
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        similarity = manager.calculate_similarity(features1, features2)
        
        assert similarity > 0.85  # Similar should be high
    
    def test_detect_new_entity(self):
        """Test detecting a new entity"""
        manager = EphemeralIdentityManager()
        
        features = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        entity_id, is_new = manager.detect_entity(features)
        
        assert is_new is True
        assert entity_id in manager.entities
        assert len(manager.entities) == 1
    
    def test_detect_existing_entity(self):
        """Test re-identifying existing entity"""
        manager = EphemeralIdentityManager()
        
        features1 = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        # First detection
        entity_id1, is_new1 = manager.detect_entity(features1)
        assert is_new1 is True
        
        # Second detection with similar features
        features2 = BehavioralFeatures(
            movement_speed=1.18,  # Very similar
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        entity_id2, is_new2 = manager.detect_entity(features2)
        
        assert is_new2 is False
        assert entity_id1 == entity_id2  # Same entity
        assert len(manager.entities) == 1  # Still only one entity
    
    def test_detect_different_entities(self):
        """Test detecting two different entities"""
        manager = EphemeralIdentityManager()
        
        features_a = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        features_b = BehavioralFeatures(
            movement_speed=0.8,  # Different
            height_estimate=1.60,  # Different
            activity_time="afternoon",
            interaction_zone="living_room",
            movement_pattern="variable"
        )
        
        entity_id_a, is_new_a = manager.detect_entity(features_a)
        entity_id_b, is_new_b = manager.detect_entity(features_b)
        
        assert is_new_a is True
        assert is_new_b is True
        assert entity_id_a != entity_id_b
        assert len(manager.entities) == 2
    
    def test_cleanup_expired_entities(self):
        """Test cleanup of expired entities"""
        manager = EphemeralIdentityManager(expiry_days=30)
        
        # Create old entity
        old_time = datetime.now() - timedelta(days=35)
        old_entity = EntityProfile(
            entity_id="old_entity",
            first_observed=old_time,
            last_seen=old_time,
            observation_count=5
        )
        manager.entities["old_entity"] = old_entity
        
        # Create recent entity
        recent_entity = EntityProfile(
            entity_id="recent_entity",
            first_observed=datetime.now(),
            last_seen=datetime.now(),
            observation_count=3
        )
        manager.entities["recent_entity"] = recent_entity
        
        # Cleanup
        expired_count = manager.cleanup_expired_entities()
        
        assert expired_count == 1
        assert "old_entity" not in manager.entities
        assert "recent_entity" in manager.entities


class TestPrivacyProperties:
    """Test privacy-preserving properties"""
    
    def test_no_biometric_data_in_features(self):
        """Verify no biometric identifiers in features"""
        features = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        # Check that no biometric fields exist
        assert not hasattr(features, 'face_embedding')
        assert not hasattr(features, 'voiceprint')
        assert not hasattr(features, 'fingerprint')
        assert not hasattr(features, 'iris_pattern')
    
    def test_no_biometric_data_in_profile(self):
        """Verify no biometric identifiers in entity profile"""
        profile = EntityProfile(
            entity_id="test_123",
            first_observed=datetime.now(),
            last_seen=datetime.now(),
            observation_count=1
        )
        
        assert not hasattr(profile, 'face_data')
        assert not hasattr(profile, 'voice_data')
        assert not hasattr(profile, 'biometric_id')
    
    def test_entity_id_not_linkable_to_identity(self):
        """Verify entity IDs cannot be linked to real identity"""
        manager = EphemeralIdentityManager()
        entity_id = manager.generate_entity_id()
        
        # Entity ID should be random string, not sequential
        assert not entity_id.isdigit()  # Not a simple number
        assert "entity_" in entity_id  # Has prefix
        
        # Should be long enough to be cryptographically random
        assert len(entity_id) > 20
    
    def test_no_persistent_event_storage(self):
        """Verify no event history is stored"""
        manager = EphemeralIdentityManager()
        
        features = BehavioralFeatures(
            movement_speed=1.2,
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        
        entity_id, _ = manager.detect_entity(features)
        profile = manager.get_entity_info(entity_id)
        
        # Should not have event log
        assert not hasattr(profile, 'event_history')
        assert not hasattr(profile, 'event_log')
        assert not hasattr(profile, 'observations_list')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
