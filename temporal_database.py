"""
Temporal Database with Future-Read (Tachyonic) and Past-Write (Quantum-Eraser) Capabilities

This module implements a theoretical temporal database that supports:
1. Tachyonic reads: Reading data from future timestamps (faster-than-light information access)
2. Quantum-eraser writes: Writing data to past timestamps (retroactive modifications)

The database maintains temporal consistency through causality tracking and version management.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
import copy


class TemporalVersion:
    """Represents a single version of data at a specific timestamp."""
    
    def __init__(self, timestamp: datetime, value: Any, causality_chain: Optional[List[datetime]] = None):
        """
        Initialize a temporal version.
        
        Args:
            timestamp: The temporal coordinate of this version
            value: The data value at this timestamp
            causality_chain: List of timestamps that led to this version
        """
        self.timestamp = timestamp
        self.value = value
        self.causality_chain = causality_chain or [timestamp]
        self.quantum_state = "superposition"  # Can be "collapsed" or "erased"
    
    def __repr__(self):
        return f"TemporalVersion(t={self.timestamp}, v={self.value}, state={self.quantum_state})"


class TemporalDatabase:
    """
    A temporal database supporting tachyonic reads and quantum-eraser writes.
    
    Features:
    - Store and retrieve data across different temporal coordinates
    - Read from future timestamps (tachyonic operations)
    - Write to past timestamps (quantum-eraser operations)
    - Maintain causality chains and temporal consistency
    - Track version history across all temporal coordinates
    """
    
    def __init__(self, reference_time: Optional[datetime] = None):
        """
        Initialize the temporal database.
        
        Args:
            reference_time: The reference "present" time (defaults to now)
        """
        self.reference_time = reference_time or datetime.now()
        # Store data with temporal versioning: key -> list of TemporalVersions
        self.temporal_store: Dict[str, List[TemporalVersion]] = {}
        # Track future-read operations (tachyonic events)
        self.tachyonic_events: List[Tuple[datetime, str]] = []
        # Track past-write operations (quantum-eraser events)
        self.quantum_eraser_events: List[Tuple[datetime, str]] = []
    
    def write(self, key: str, value: Any, timestamp: Optional[datetime] = None) -> bool:
        """
        Write data at a specific temporal coordinate.
        
        Args:
            key: Data identifier
            value: Data value to store
            timestamp: Temporal coordinate (defaults to reference time)
            
        Returns:
            bool: Success status
        """
        if timestamp is None:
            timestamp = self.reference_time
        
        version = TemporalVersion(timestamp, value)
        
        if key not in self.temporal_store:
            self.temporal_store[key] = []
        
        # Insert version in temporal order
        self.temporal_store[key].append(version)
        self.temporal_store[key].sort(key=lambda v: v.timestamp)
        
        return True
    
    def read(self, key: str, timestamp: Optional[datetime] = None) -> Optional[Any]:
        """
        Read data at a specific temporal coordinate.
        
        Args:
            key: Data identifier
            timestamp: Temporal coordinate (defaults to reference time)
            
        Returns:
            The value at the specified timestamp, or None if not found
        """
        if timestamp is None:
            timestamp = self.reference_time
        
        if key not in self.temporal_store:
            return None
        
        versions = self.temporal_store[key]
        
        # Find the most recent version at or before the requested timestamp
        valid_versions = [v for v in versions if v.timestamp <= timestamp]
        
        if not valid_versions:
            return None
        
        return valid_versions[-1].value
    
    def tachyonic_read(self, key: str, future_offset: timedelta) -> Optional[Any]:
        """
        Perform a tachyonic read - read data from a future timestamp.
        
        This simulates faster-than-light information access by reading data
        that exists at a future temporal coordinate.
        
        Args:
            key: Data identifier
            future_offset: How far into the future to read
            
        Returns:
            The value at the future timestamp, or None if not found
        """
        future_timestamp = self.reference_time + future_offset
        
        # Record this tachyonic event
        self.tachyonic_events.append((future_timestamp, key))
        
        return self.read(key, future_timestamp)
    
    def quantum_eraser_write(self, key: str, value: Any, past_offset: timedelta) -> bool:
        """
        Perform a quantum-eraser write - write data to a past timestamp.
        
        This simulates retroactive modification by inserting or modifying data
        at a past temporal coordinate, similar to quantum erasure experiments.
        
        Args:
            key: Data identifier
            value: Data value to store
            past_offset: How far into the past to write (negative or positive)
            
        Returns:
            bool: Success status
        """
        # Calculate the past timestamp
        if isinstance(past_offset, timedelta):
            past_timestamp = self.reference_time - past_offset
        else:
            # If it's already a datetime, use it directly
            past_timestamp = past_offset
        
        # Record this quantum-eraser event
        self.quantum_eraser_events.append((past_timestamp, key))
        
        # Perform the write operation
        success = self.write(key, value, past_timestamp)
        
        if success and key in self.temporal_store:
            # Mark affected future versions for causality recalculation
            for version in self.temporal_store[key]:
                if version.timestamp > past_timestamp:
                    # Add the past write to the causality chain
                    if past_timestamp not in version.causality_chain:
                        version.causality_chain.append(past_timestamp)
                        version.causality_chain.sort()
        
        return success
    
    def get_temporal_history(self, key: str) -> List[TemporalVersion]:
        """
        Get the complete temporal history of a key.
        
        Args:
            key: Data identifier
            
        Returns:
            List of all temporal versions for this key
        """
        if key not in self.temporal_store:
            return []
        
        return copy.deepcopy(self.temporal_store[key])
    
    def collapse_quantum_state(self, key: str, timestamp: datetime) -> bool:
        """
        Collapse the quantum state of a specific version.
        
        Args:
            key: Data identifier
            timestamp: Temporal coordinate of the version to collapse
            
        Returns:
            bool: Success status
        """
        if key not in self.temporal_store:
            return False
        
        for version in self.temporal_store[key]:
            if version.timestamp == timestamp:
                version.quantum_state = "collapsed"
                return True
        
        return False
    
    def erase_quantum_state(self, key: str, timestamp: datetime) -> bool:
        """
        Erase the quantum state of a specific version.
        
        Args:
            key: Data identifier
            timestamp: Temporal coordinate of the version to erase
            
        Returns:
            bool: Success status
        """
        if key not in self.temporal_store:
            return False
        
        for version in self.temporal_store[key]:
            if version.timestamp == timestamp:
                version.quantum_state = "erased"
                return True
        
        return False
    
    def get_causality_chain(self, key: str, timestamp: datetime) -> List[datetime]:
        """
        Get the causality chain for a specific version.
        
        Args:
            key: Data identifier
            timestamp: Temporal coordinate
            
        Returns:
            List of timestamps in the causality chain
        """
        if key not in self.temporal_store:
            return []
        
        for version in self.temporal_store[key]:
            if version.timestamp == timestamp:
                return version.causality_chain.copy()
        
        return []
    
    def get_tachyonic_events(self) -> List[Tuple[datetime, str]]:
        """
        Get all recorded tachyonic (future-read) events.
        
        Returns:
            List of (timestamp, key) tuples
        """
        return self.tachyonic_events.copy()
    
    def get_quantum_eraser_events(self) -> List[Tuple[datetime, str]]:
        """
        Get all recorded quantum-eraser (past-write) events.
        
        Returns:
            List of (timestamp, key) tuples
        """
        return self.quantum_eraser_events.copy()


if __name__ == "__main__":
    print("=" * 70)
    print("TEMPORAL DATABASE - Tachyonic Reads & Quantum-Eraser Writes")
    print("=" * 70)
    print()
    
    # Initialize the temporal database
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = TemporalDatabase(reference_time=reference_time)
    
    print(f"Reference Time (Present): {reference_time}")
    print()
    
    # Standard write at reference time
    print("1. Standard Write Operation:")
    db.write("user_status", "online", reference_time)
    print(f"   Written 'online' at {reference_time}")
    print(f"   Current status: {db.read('user_status')}")
    print()
    
    # Write to future
    print("2. Writing to Future:")
    future_time = reference_time + timedelta(hours=2)
    db.write("user_status", "offline", future_time)
    print(f"   Written 'offline' at {future_time}")
    print()
    
    # Tachyonic read (read from future)
    print("3. Tachyonic Read (Future-Read):")
    future_status = db.tachyonic_read("user_status", timedelta(hours=2))
    print(f"   Reading 2 hours into the future...")
    print(f"   Future status: {future_status}")
    print()
    
    # Quantum-eraser write (write to past)
    print("4. Quantum-Eraser Write (Past-Write):")
    db.quantum_eraser_write("user_status", "away", timedelta(hours=1))
    print(f"   Written 'away' 1 hour into the past")
    past_time = reference_time - timedelta(hours=1)
    print(f"   Status at {past_time}: {db.read('user_status', past_time)}")
    print()
    
    # Show temporal history
    print("5. Temporal History:")
    history = db.get_temporal_history("user_status")
    for version in history:
        print(f"   {version}")
    print()
    
    # Show causality chains
    print("6. Causality Tracking:")
    for version in history:
        chain = db.get_causality_chain("user_status", version.timestamp)
        print(f"   At {version.timestamp}: causality chain = {chain}")
    print()
    
    # Show recorded events
    print("7. Event Log:")
    print(f"   Tachyonic events: {len(db.get_tachyonic_events())}")
    for event_time, key in db.get_tachyonic_events():
        print(f"      - Future read of '{key}' at {event_time}")
    
    print(f"   Quantum-eraser events: {len(db.get_quantum_eraser_events())}")
    for event_time, key in db.get_quantum_eraser_events():
        print(f"      - Past write of '{key}' at {event_time}")
    print()
    
    print("=" * 70)
    print("Temporal operations demonstrate the paradoxical nature of")
    print("causality in a database that transcends linear time.")
    print("=" * 70)
