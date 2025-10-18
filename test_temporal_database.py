"""
Test suite for Temporal Database with Future-Read and Past-Write capabilities
"""

from datetime import datetime, timedelta
import temporal_database


def test_basic_write_read():
    """Test basic write and read operations"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write data
    assert db.write("key1", "value1") == True
    
    # Read data
    assert db.read("key1") == "value1"
    
    # Read non-existent key
    assert db.read("nonexistent") is None


def test_temporal_write_read():
    """Test write and read at specific timestamps"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write at different timestamps
    past_time = reference_time - timedelta(hours=1)
    future_time = reference_time + timedelta(hours=1)
    
    db.write("status", "past_value", past_time)
    db.write("status", "present_value", reference_time)
    db.write("status", "future_value", future_time)
    
    # Read at different timestamps
    assert db.read("status", past_time) == "past_value"
    assert db.read("status", reference_time) == "present_value"
    assert db.read("status", future_time) == "future_value"


def test_tachyonic_read():
    """Test future-read (tachyonic) operations"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write data in the future
    future_time = reference_time + timedelta(hours=2)
    db.write("future_data", "from_the_future", future_time)
    
    # Perform tachyonic read
    result = db.tachyonic_read("future_data", timedelta(hours=2))
    assert result == "from_the_future"
    
    # Verify the tachyonic event was recorded
    events = db.get_tachyonic_events()
    assert len(events) == 1
    assert events[0][0] == future_time
    assert events[0][1] == "future_data"


def test_quantum_eraser_write():
    """Test past-write (quantum-eraser) operations"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write to the present
    db.write("data", "present", reference_time)
    
    # Perform quantum-eraser write (write to the past)
    success = db.quantum_eraser_write("data", "retroactive", timedelta(hours=1))
    assert success == True
    
    # Verify the past data exists
    past_time = reference_time - timedelta(hours=1)
    assert db.read("data", past_time) == "retroactive"
    
    # Verify the quantum-eraser event was recorded
    events = db.get_quantum_eraser_events()
    assert len(events) == 1
    assert events[0][1] == "data"


def test_temporal_history():
    """Test temporal history retrieval"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write multiple versions
    times = [
        reference_time - timedelta(hours=2),
        reference_time - timedelta(hours=1),
        reference_time,
        reference_time + timedelta(hours=1),
    ]
    
    for i, t in enumerate(times):
        db.write("versioned", f"version_{i}", t)
    
    # Get history
    history = db.get_temporal_history("versioned")
    assert len(history) == 4
    
    # Verify chronological order
    for i in range(len(history) - 1):
        assert history[i].timestamp < history[i + 1].timestamp


def test_causality_chain():
    """Test causality chain tracking"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write to present
    db.write("causal", "present", reference_time)
    
    # Write to future
    future_time = reference_time + timedelta(hours=1)
    db.write("causal", "future", future_time)
    
    # Quantum-eraser write to past
    past_time = reference_time - timedelta(hours=1)
    db.quantum_eraser_write("causal", "past", timedelta(hours=1))
    
    # Check causality chain for future version
    chain = db.get_causality_chain("causal", future_time)
    assert past_time in chain


def test_quantum_state_operations():
    """Test quantum state collapse and erasure"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write data
    db.write("quantum", "superposition", reference_time)
    
    # Collapse quantum state
    assert db.collapse_quantum_state("quantum", reference_time) == True
    
    # Check the state
    history = db.get_temporal_history("quantum")
    assert len(history) == 1
    assert history[0].quantum_state == "collapsed"
    
    # Erase quantum state
    assert db.erase_quantum_state("quantum", reference_time) == True
    
    # Check the state again
    history = db.get_temporal_history("quantum")
    assert history[0].quantum_state == "erased"


def test_temporal_version_ordering():
    """Test that temporal versions are kept in chronological order"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write in non-chronological order
    db.write("ordered", "third", reference_time + timedelta(hours=2))
    db.write("ordered", "first", reference_time)
    db.write("ordered", "second", reference_time + timedelta(hours=1))
    
    # Get history and verify order
    history = db.get_temporal_history("ordered")
    assert len(history) == 3
    assert history[0].value == "first"
    assert history[1].value == "second"
    assert history[2].value == "third"


def test_read_interpolation():
    """Test reading between written timestamps"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write at two timestamps
    time1 = reference_time
    time2 = reference_time + timedelta(hours=2)
    
    db.write("interpolate", "value1", time1)
    db.write("interpolate", "value2", time2)
    
    # Read at a time between the two writes
    between_time = reference_time + timedelta(hours=1)
    result = db.read("interpolate", between_time)
    
    # Should get the most recent value before the requested time
    assert result == "value1"


def test_multiple_tachyonic_reads():
    """Test multiple tachyonic read operations"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Write future data
    for i in range(5):
        future_time = reference_time + timedelta(hours=i+1)
        db.write("future", f"value_{i+1}", future_time)
    
    # Perform multiple tachyonic reads
    for i in range(5):
        result = db.tachyonic_read("future", timedelta(hours=i+1))
        assert result == f"value_{i+1}"
    
    # Verify all events were recorded
    events = db.get_tachyonic_events()
    assert len(events) == 5


def test_multiple_quantum_eraser_writes():
    """Test multiple quantum-eraser write operations"""
    reference_time = datetime(2025, 1, 1, 12, 0, 0)
    db = temporal_database.TemporalDatabase(reference_time=reference_time)
    
    # Perform multiple quantum-eraser writes
    for i in range(5):
        db.quantum_eraser_write("past", f"value_{i+1}", timedelta(hours=i+1))
    
    # Verify all events were recorded
    events = db.get_quantum_eraser_events()
    assert len(events) == 5
    
    # Verify data integrity
    for i in range(5):
        past_time = reference_time - timedelta(hours=i+1)
        result = db.read("past", past_time)
        assert result == f"value_{i+1}"


if __name__ == "__main__":
    # Run all tests
    test_basic_write_read()
    print("✓ Basic write/read tests passed")
    
    test_temporal_write_read()
    print("✓ Temporal write/read tests passed")
    
    test_tachyonic_read()
    print("✓ Tachyonic read tests passed")
    
    test_quantum_eraser_write()
    print("✓ Quantum-eraser write tests passed")
    
    test_temporal_history()
    print("✓ Temporal history tests passed")
    
    test_causality_chain()
    print("✓ Causality chain tests passed")
    
    test_quantum_state_operations()
    print("✓ Quantum state operation tests passed")
    
    test_temporal_version_ordering()
    print("✓ Temporal version ordering tests passed")
    
    test_read_interpolation()
    print("✓ Read interpolation tests passed")
    
    test_multiple_tachyonic_reads()
    print("✓ Multiple tachyonic reads tests passed")
    
    test_multiple_quantum_eraser_writes()
    print("✓ Multiple quantum-eraser writes tests passed")
    
    print("\n" + "=" * 60)
    print("All temporal database tests passed successfully! ✓")
    print("=" * 60)
