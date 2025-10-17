"""
Unit tests for Elliptic Curve Celestial Mechanics

Basic tests to verify the implementation works correctly.
"""

import numpy as np
from elliptic_curve_celestial_mechanics import (
    EllipticOrbit,
    AlgebraicCurve,
    EllipticIntegrals,
    OrbitalMechanics
)


def test_elliptic_orbit_creation():
    """Test creating an elliptic orbit."""
    print("Testing EllipticOrbit creation...")
    orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.5)
    assert orbit.a == 1.0
    assert orbit.e == 0.5
    assert abs(orbit.b - 0.866025) < 0.001
    print("✓ EllipticOrbit creation test passed")


def test_elliptic_orbit_validation():
    """Test that invalid eccentricity raises error."""
    print("Testing EllipticOrbit validation...")
    try:
        orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=1.5)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ EllipticOrbit validation test passed")


def test_periapsis_apoapsis():
    """Test periapsis and apoapsis calculations."""
    print("Testing periapsis and apoapsis...")
    orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.2)
    assert abs(orbit.periapsis() - 0.8) < 0.001
    assert abs(orbit.apoapsis() - 1.2) < 0.001
    print("✓ Periapsis and apoapsis test passed")


def test_radial_distance():
    """Test radial distance calculations."""
    print("Testing radial distance...")
    orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.0)
    # For circular orbit, distance should be constant
    r0 = orbit.radial_distance(0)
    r90 = orbit.radial_distance(np.pi/2)
    assert abs(r0 - 1.0) < 0.001
    assert abs(r90 - 1.0) < 0.001
    print("✓ Radial distance test passed")


def test_keplers_equation():
    """Test solving Kepler's equation."""
    print("Testing Kepler's equation solver...")
    orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.3)
    # At mean anomaly = 0, eccentric anomaly should also be 0
    E = orbit.eccentric_anomaly_from_mean(0.0)
    assert abs(E) < 0.001
    # At mean anomaly = π, eccentric anomaly should be π
    E = orbit.eccentric_anomaly_from_mean(np.pi)
    assert abs(E - np.pi) < 0.001
    print("✓ Kepler's equation test passed")


def test_true_anomaly_conversion():
    """Test conversion from eccentric to true anomaly."""
    print("Testing true anomaly conversion...")
    orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.3)
    # At E = 0, true anomaly should be 0
    theta = orbit.true_anomaly_from_eccentric(0.0)
    assert abs(theta) < 0.001
    # At E = π, true anomaly should be π
    theta = orbit.true_anomaly_from_eccentric(np.pi)
    assert abs(theta - np.pi) < 0.001
    print("✓ True anomaly conversion test passed")


def test_algebraic_curve():
    """Test algebraic curve representation."""
    print("Testing algebraic curve...")
    curve = AlgebraicCurve.from_ellipse(a=2.0, b=1.5)
    assert curve.curve_type() == "Ellipse"
    assert curve.discriminant() < 0
    print("✓ Algebraic curve test passed")


def test_elliptic_integrals():
    """Test elliptic integral calculations."""
    print("Testing elliptic integrals...")
    # For k=0, both K(0) and E(0) should equal π/2
    K = EllipticIntegrals.complete_elliptic_integral_first_kind(0.0)
    E = EllipticIntegrals.complete_elliptic_integral_second_kind(0.0)
    assert abs(K - np.pi/2) < 0.001
    assert abs(E - np.pi/2) < 0.001
    print("✓ Elliptic integrals test passed")


def test_ellipse_perimeter():
    """Test ellipse perimeter calculation."""
    print("Testing ellipse perimeter...")
    # For a circle (a=b), perimeter should be 2πr
    perimeter = EllipticIntegrals.ellipse_perimeter(1.0, 1.0)
    assert abs(perimeter - 2*np.pi) < 0.001
    print("✓ Ellipse perimeter test passed")


def test_vis_viva():
    """Test vis-viva equation."""
    print("Testing vis-viva equation...")
    mu = 1.0
    a = 1.0
    # For circular orbit at r=a, v² = μ/a
    v = OrbitalMechanics.vis_viva_equation(a, a, mu)
    expected_v = np.sqrt(mu/a)
    assert abs(v - expected_v) < 0.001
    print("✓ Vis-viva equation test passed")


def test_orbital_energy():
    """Test specific orbital energy calculation."""
    print("Testing orbital energy...")
    mu = 1.0
    a = 1.0
    energy = OrbitalMechanics.specific_orbital_energy(a, mu)
    expected = -mu / (2*a)
    assert abs(energy - expected) < 0.001
    print("✓ Orbital energy test passed")


def test_angular_momentum():
    """Test specific angular momentum calculation."""
    print("Testing angular momentum...")
    mu = 1.0
    a = 1.0
    e = 0.0
    h = OrbitalMechanics.specific_angular_momentum(a, e, mu)
    expected = np.sqrt(mu * a)
    assert abs(h - expected) < 0.001
    print("✓ Angular momentum test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("Running Elliptic Curve Celestial Mechanics Tests")
    print("=" * 70 + "\n")
    
    tests = [
        test_elliptic_orbit_creation,
        test_elliptic_orbit_validation,
        test_periapsis_apoapsis,
        test_radial_distance,
        test_keplers_equation,
        test_true_anomaly_conversion,
        test_algebraic_curve,
        test_elliptic_integrals,
        test_ellipse_perimeter,
        test_vis_viva,
        test_orbital_energy,
        test_angular_momentum,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
