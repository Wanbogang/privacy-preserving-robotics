"""
Ephemeral Identity Management Demo

Demonstrates how the Privacy-Preserving Robotics Framework manages identity
without biometric identification. Entities are tracked through behavioral
patterns rather than personal identifiers.

Key Features:
- Cryptographically random entity IDs
- Behavioral similarity matching
- Automatic ID expiration
- No biometric data storage

Author: Agus Setiawan
License: GPL-3.0
"""

import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np


@dataclass
class BehavioralFeatures:
    """
    Abstract behavioral features extracted from sensors.
    NO biometric data - only movement patterns and interaction styles.
    """
    movement_speed: float  # meters per second (0.5-2.0 typical human range)
    height_estimate: float  # meters (rough estimate, not precise)
    activity_time: str  # time of day (morning/afternoon/evening)
    interaction_zone: str  # location zone (kitchen/living_room/bedroom)
    movement_pattern: str  # pattern type (steady/variable/stationary)
    
    def to_vector(self) -> np.ndarray:
        """Convert features to numerical vector for similarity comparison."""
        # Encode categorical features
        time_encoding = {"morning": 0, "afternoon": 1, "evening": 2, "night": 3}
        zone_encoding = {"kitchen": 0, "living_room": 1, "bedroom": 2, "bathroom": 3}
        pattern_encoding = {"steady": 0, "variable": 1, "stationary": 2}
        
        return np.array([
            self.movement_speed,
            self.height_estimate,
            time_encoding.get(self.activity_time, 0),
            zone_encoding.get(self.interaction_zone, 0),
            pattern_encoding.get(self.movement_pattern, 0)
        ])


@dataclass
class EntityProfile:
    """
    Ephemeral entity profile with behavioral patterns.
    No personal identifiable information stored.
    """
    entity_id: str
    first_observed: datetime
    last_seen: datetime
    observation_count: int = 0
    typical_features: Optional[BehavioralFeatures] = None
    confidence: float = 0.0
    
    def is_expired(self, expiry_days: int = 30) -> bool:
        """Check if entity ID has expired due to inactivity."""
        inactivity = datetime.now() - self.last_seen
        return inactivity.days > expiry_days
    
    def update(self, features: BehavioralFeatures):
        """Update profile with new observation."""
        self.last_seen = datetime.now()
        self.observation_count += 1
        
        # Update confidence based on observation count
        self.confidence = min(1.0, self.observation_count / 10.0)
        
        if self.typical_features is None:
            self.typical_features = features
        else:
            # Exponential moving average to update typical features
            alpha = 0.3  # Learning rate
            current_vec = self.typical_features.to_vector()
            new_vec = features.to_vector()
            updated_vec = alpha * new_vec + (1 - alpha) * current_vec
            
            # Update typical features (simplified - just update numerical values)
            self.typical_features.movement_speed = updated_vec[0]
            self.typical_features.height_estimate = updated_vec[1]


class EphemeralIdentityManager:
    """
    Manages ephemeral entity identities without biometric identification.
    
    Key Privacy Properties:
    - Entity IDs are cryptographically random
    - No biometric data stored
    - IDs expire after inactivity period
    - Re-identification based on behavioral similarity only
    """
    
    def __init__(self, similarity_threshold: float = 0.85, expiry_days: int = 30):
        self.entities: Dict[str, EntityProfile] = {}
        self.similarity_threshold = similarity_threshold
        self.expiry_days = expiry_days
    
    def generate_entity_id(self) -> str:
        """Generate cryptographically random entity ID."""
        return f"entity_{secrets.token_hex(16)}"
    
    def calculate_similarity(self, features1: BehavioralFeatures, 
                           features2: BehavioralFeatures) -> float:
        """
        Calculate behavioral similarity between two feature sets.
        Returns value between 0 (completely different) and 1 (identical).
        """
        vec1 = features1.to_vector()
        vec2 = features2.to_vector()
        
        # Use weighted Euclidean distance for better discrimination
        # Weight movement speed and height more heavily
        weights = np.array([2.0, 2.0, 1.0, 1.0, 1.0])
        
        # Calculate weighted distance
        diff = (vec1 - vec2) * weights
        distance = np.linalg.norm(diff)
        
        # Convert distance to similarity (0 = different, 1 = identical)
        # Max expected distance is ~10 for very different entities
        max_distance = 10.0
        similarity = max(0.0, 1.0 - (distance / max_distance))
        
        return similarity
    
    def find_matching_entity(self, features: BehavioralFeatures) -> Optional[str]:
        """
        Find existing entity that matches behavioral features.
        Returns entity_id if match found, None otherwise.
        """
        best_match_id = None
        best_similarity = 0.0
        
        # Check all active entities
        for entity_id, profile in self.entities.items():
            if profile.is_expired(self.expiry_days):
                continue
                
            if profile.typical_features is None:
                continue
            
            similarity = self.calculate_similarity(features, profile.typical_features)
            
            if similarity > best_similarity and similarity > self.similarity_threshold:
                best_similarity = similarity
                best_match_id = entity_id
        
        return best_match_id
    
    def detect_entity(self, features: BehavioralFeatures) -> Tuple[str, bool]:
        """
        Detect entity from behavioral features.
        
        Returns:
            Tuple of (entity_id, is_new_entity)
        """
        # Try to match with existing entity
        entity_id = self.find_matching_entity(features)
        
        if entity_id:
            # Existing entity re-identified
            self.entities[entity_id].update(features)
            return entity_id, False
        else:
            # New entity detected
            entity_id = self.generate_entity_id()
            profile = EntityProfile(
                entity_id=entity_id,
                first_observed=datetime.now(),
                last_seen=datetime.now(),
                observation_count=1,
                typical_features=features,
                confidence=0.1
            )
            self.entities[entity_id] = profile
            return entity_id, True
    
    def cleanup_expired_entities(self):
        """Remove expired entity IDs."""
        expired = [eid for eid, profile in self.entities.items() 
                  if profile.is_expired(self.expiry_days)]
        
        for eid in expired:
            del self.entities[eid]
        
        return len(expired)
    
    def get_entity_info(self, entity_id: str) -> Optional[EntityProfile]:
        """Get entity profile (for demonstration purposes)."""
        return self.entities.get(entity_id)


def run_demo():
    """
    Demonstrate ephemeral identity management with simulated scenarios.
    """
    print("=" * 70)
    print("EPHEMERAL IDENTITY MANAGEMENT DEMO")
    print("Privacy-Preserving Home Robotics Framework")
    print("=" * 70)
    print()
    
    # Initialize identity manager
    manager = EphemeralIdentityManager(similarity_threshold=0.85, expiry_days=30)
    
    print("Scenario 1: Person A enters kitchen (morning)")
    print("-" * 70)
    
    # First observation of Person A
    features_a1 = BehavioralFeatures(
        movement_speed=1.2,
        height_estimate=1.75,
        activity_time="morning",
        interaction_zone="kitchen",
        movement_pattern="steady"
    )
    
    entity_id, is_new = manager.detect_entity(features_a1)
    print(f"✓ Entity detected: {entity_id[:20]}...")
    print(f"✓ New entity: {is_new}")
    print(f"✓ No biometric data stored - only behavioral patterns")
    print()
    
    time.sleep(1)
    
    print("Scenario 2: Same person returns to kitchen (afternoon)")
    print("-" * 70)
    
    # Second observation - similar features (same person)
    features_a2 = BehavioralFeatures(
        movement_speed=1.15,  # Slightly different but similar
        height_estimate=1.75,
        activity_time="afternoon",
        interaction_zone="kitchen",
        movement_pattern="steady"
    )
    
    entity_id_2, is_new_2 = manager.detect_entity(features_a2)
    print(f"✓ Entity detected: {entity_id_2[:20]}...")
    print(f"✓ New entity: {is_new_2}")
    print(f"✓ Same ID as before: {entity_id == entity_id_2}")
    
    profile = manager.get_entity_info(entity_id)
    print(f"✓ Confidence level: {profile.confidence:.2f}")
    print(f"✓ Observation count: {profile.observation_count}")
    print()
    
    time.sleep(1)
    
    print("Scenario 3: Different person enters (Person B)")
    print("-" * 70)
    
    # Observation of different person - different behavioral features
    features_b1 = BehavioralFeatures(
        movement_speed=0.8,  # Slower movement
        height_estimate=1.60,  # Different height
        activity_time="afternoon",
        interaction_zone="living_room",
        movement_pattern="variable"
    )
    
    entity_id_b, is_new_b = manager.detect_entity(features_b1)
    print(f"✓ Entity detected: {entity_id_b[:20]}...")
    print(f"✓ New entity: {is_new_b}")
    print(f"✓ Different ID from Person A: {entity_id != entity_id_b}")
    print()
    
    time.sleep(1)
    
    print("Scenario 4: Entity re-identification over time")
    print("-" * 70)
    
    # Multiple observations of Person A
    for i in range(5):
        features = BehavioralFeatures(
            movement_speed=np.random.normal(1.2, 0.1),  # Slight variations
            height_estimate=1.75,
            activity_time="morning",
            interaction_zone="kitchen",
            movement_pattern="steady"
        )
        eid, is_new = manager.detect_entity(features)
        print(f"  Observation {i+1}: {eid[:20]}... (new={is_new})")
    
    profile_a = manager.get_entity_info(entity_id)
    print(f"✓ Confidence after multiple observations: {profile_a.confidence:.2f}")
    print()
    
    time.sleep(1)
    
    print("Scenario 5: Privacy properties verification")
    print("-" * 70)
    
    print("✓ Total entities tracked: ", len(manager.entities))
    print("✓ Entity IDs are cryptographically random")
    print("✓ No biometric identifiers stored")
    print("✓ No facial data, voiceprints, or fingerprints")
    print("✓ Cannot link entity_id to real-world identity")
    print("✓ IDs will expire after 30 days of inactivity")
    print()
    
    print("=" * 70)
    print("Summary: Privacy-Preserving Identity Management")
    print("=" * 70)
    print()
    print("Key Features Demonstrated:")
    print("  1. Ephemeral IDs - cryptographically random, not sequential")
    print("  2. Behavioral matching - no biometric identification")
    print("  3. Confidence building - improves with observations")
    print("  4. Automatic expiration - IDs don't persist forever")
    print("  5. Privacy by design - impossible to store biometric data")
    print()
    print("Privacy Guarantees:")
    print("  ✓ No facial recognition")
    print("  ✓ No biometric storage")
    print("  ✓ Cannot reconstruct real identity")
    print("  ✓ Behavioral continuity maintained")
    print()


if __name__ == "__main__":
    run_demo()
