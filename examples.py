"""
Examples and demonstrations of Elliptic Curves in Celestial Mechanics

This file provides various examples of using the elliptic curve
implementations for celestial mechanics calculations.
"""

import numpy as np
from elliptic_curve_celestial_mechanics import (
    EllipticOrbit,
    AlgebraicCurve,
    EllipticIntegrals,
    OrbitalMechanics
)


def example_planetary_orbits():
    """Demonstrate calculations for real planetary orbits."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Real Planetary Orbits")
    print("=" * 70)
    
    planets = {
        "Mercury": {"a": 0.387, "e": 0.206},
        "Venus": {"a": 0.723, "e": 0.007},
        "Earth": {"a": 1.000, "e": 0.017},
        "Mars": {"a": 1.524, "e": 0.093},
        "Jupiter": {"a": 5.203, "e": 0.048},
        "Saturn": {"a": 9.537, "e": 0.054},
    }
    
    print("\nPlanetary Orbital Parameters (Semi-major axis in AU):")
    print("-" * 70)
    print(f"{'Planet':<10} {'a (AU)':<10} {'e':<10} {'Perihelion':<12} {'Aphelion':<12}")
    print("-" * 70)
    
    for planet, params in planets.items():
        orbit = EllipticOrbit(params["a"], params["e"])
        print(f"{planet:<10} {orbit.a:<10.3f} {orbit.e:<10.3f} "
              f"{orbit.periapsis():<12.3f} {orbit.apoapsis():<12.3f}")
    
    print("\n")


def example_comet_orbit():
    """Demonstrate calculations for a highly eccentric comet orbit."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Halley's Comet - Highly Eccentric Orbit")
    print("=" * 70)
    
    # Halley's Comet parameters
    halley = EllipticOrbit(semi_major_axis=17.8, eccentricity=0.967)
    
    print(f"\nOrbital Parameters:")
    print(f"  Semi-major axis (a): {halley.a} AU")
    print(f"  Semi-minor axis (b): {halley.b:.3f} AU")
    print(f"  Eccentricity (e): {halley.e}")
    print(f"  Linear eccentricity (c): {halley.c:.3f} AU")
    print(f"  Perihelion distance: {halley.periapsis():.3f} AU")
    print(f"  Aphelion distance: {halley.apoapsis():.3f} AU")
    
    # Calculate positions at various true anomalies
    print(f"\nPosition at various points in orbit:")
    print(f"  {'True Anomaly':<20} {'Distance (AU)':<15} {'x (AU)':<12} {'y (AU)':<12}")
    print("-" * 70)
    
    for degrees in [0, 45, 90, 135, 180]:
        theta = np.radians(degrees)
        r = halley.radial_distance(theta)
        x, y = halley.cartesian_coordinates(theta)
        print(f"  {degrees:>3}° ({theta:6.3f} rad)  {r:>12.3f}    {x:>10.3f}  {y:>10.3f}")
    
    print("\n")


def example_orbital_period():
    """Calculate orbital periods for various orbits."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Orbital Period Calculations")
    print("=" * 70)
    
    # Using solar mass for gravitational parameter
    # μ_sun = G * M_sun ≈ 1.327 × 10^20 m³/s² ≈ 4π²/T_year² (in AU³/year² units)
    mu_sun = 4 * np.pi**2  # AU³/year²
    
    orbits = [
        ("Inner circular", 0.5, 0.0),
        ("Earth-like", 1.0, 0.017),
        ("Mars-like", 1.524, 0.093),
        ("Comet (eccentric)", 5.0, 0.8),
    ]
    
    print(f"\n{'Orbit Type':<20} {'a (AU)':<10} {'e':<10} {'Period (years)':<15}")
    print("-" * 70)
    
    for name, a, e in orbits:
        orbit = EllipticOrbit(a, e)
        period = orbit.orbital_period(mu_sun)
        print(f"{name:<20} {a:<10.3f} {e:<10.3f} {period:<15.3f}")
    
    print("\n")


def example_keplers_equation():
    """Demonstrate solving Kepler's equation."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Solving Kepler's Equation")
    print("=" * 70)
    
    orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.3)
    
    print(f"\nOrbit: a = {orbit.a} AU, e = {orbit.e}")
    print(f"\nConverting Mean Anomaly → Eccentric Anomaly → True Anomaly:")
    print(f"{'M (rad)':<12} {'M (deg)':<12} {'E (rad)':<12} {'E (deg)':<12} "
          f"{'θ (rad)':<12} {'θ (deg)':<12}")
    print("-" * 80)
    
    for M_deg in [0, 30, 60, 90, 120, 150, 180]:
        M = np.radians(M_deg)
        E = orbit.eccentric_anomaly_from_mean(M)
        theta = orbit.true_anomaly_from_eccentric(E)
        
        print(f"{M:>10.4f}  {M_deg:>10.1f}  {E:>10.4f}  {np.degrees(E):>10.1f}  "
              f"{theta:>10.4f}  {np.degrees(theta):>10.1f}")
    
    print("\n")


def example_algebraic_curves():
    """Demonstrate algebraic curve representations."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Algebraic Curve Representations")
    print("=" * 70)
    
    curves = [
        ("Circle", 1.0, 1.0),
        ("Ellipse (wide)", 3.0, 2.0),
        ("Ellipse (narrow)", 5.0, 1.0),
    ]
    
    print(f"\n{'Curve Type':<20} {'a':<8} {'b':<8} {'Discriminant':<15} {'Type':<10}")
    print("-" * 70)
    
    for name, a, b in curves:
        curve = AlgebraicCurve.from_ellipse(a, b)
        disc = curve.discriminant()
        ctype = curve.curve_type()
        print(f"{name:<20} {a:<8.2f} {b:<8.2f} {disc:<15.6f} {ctype:<10}")
    
    # Show equation coefficients
    print(f"\nAlgebraic equation Ax² + Bxy + Cy² + Dx + Ey + F = 0")
    print(f"For ellipse with a=3.0, b=2.0:")
    curve = AlgebraicCurve.from_ellipse(3.0, 2.0)
    print(f"  A = {curve.A}")
    print(f"  B = {curve.B}")
    print(f"  C = {curve.C}")
    print(f"  D = {curve.D}")
    print(f"  E = {curve.E}")
    print(f"  F = {curve.F}")
    
    print("\n")


def example_elliptic_integrals():
    """Demonstrate elliptic integral calculations."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Elliptic Integrals")
    print("=" * 70)
    
    print(f"\nComplete Elliptic Integrals of First and Second Kind:")
    print(f"{'k':<10} {'K(k)':<20} {'E(k)':<20}")
    print("-" * 50)
    
    for k in [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]:
        K = EllipticIntegrals.complete_elliptic_integral_first_kind(k)
        E = EllipticIntegrals.complete_elliptic_integral_second_kind(k)
        print(f"{k:<10.2f} {K:<20.10f} {E:<20.10f}")
    
    print(f"\nEllipse Perimeter Calculations:")
    print(f"{'a':<10} {'b':<10} {'Perimeter':<20}")
    print("-" * 40)
    
    for a, b in [(1.0, 1.0), (2.0, 1.0), (3.0, 2.0), (5.0, 3.0)]:
        perimeter = EllipticIntegrals.ellipse_perimeter(a, b)
        print(f"{a:<10.2f} {b:<10.2f} {perimeter:<20.10f}")
    
    print("\n")


def example_orbital_velocity():
    """Demonstrate orbital velocity calculations."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Orbital Velocity (Vis-Viva Equation)")
    print("=" * 70)
    
    # Earth-Sun system (normalized units)
    mu = 4 * np.pi**2  # AU³/year²
    orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.0167)
    
    print(f"\nOrbit: a = {orbit.a} AU, e = {orbit.e}")
    print(f"Standard gravitational parameter: μ = {mu:.4f} AU³/year²")
    
    print(f"\n{'Position':<15} {'r (AU)':<12} {'v (AU/year)':<15} {'v (km/s)':<12}")
    print("-" * 60)
    
    # Calculate at perihelion, mean distance, and aphelion
    positions = [
        ("Perihelion", orbit.periapsis()),
        ("Mean", orbit.a),
        ("Aphelion", orbit.apoapsis()),
    ]
    
    for name, r in positions:
        v = OrbitalMechanics.vis_viva_equation(r, orbit.a, mu)
        # Convert AU/year to km/s (1 AU ≈ 149.6e6 km, 1 year ≈ 365.25*24*3600 s)
        v_km_s = v * 149.6e6 / (365.25 * 24 * 3600)
        print(f"{name:<15} {r:<12.6f} {v:<15.6f} {v_km_s:<12.3f}")
    
    print("\n")


def example_orbital_energy():
    """Demonstrate orbital energy calculations."""
    print("\n" + "=" * 70)
    print("EXAMPLE: Orbital Energy and Angular Momentum")
    print("=" * 70)
    
    mu = 1.0  # Normalized units
    
    orbits = [
        ("Circular", 1.0, 0.0),
        ("Slightly elliptic", 1.0, 0.1),
        ("Moderately elliptic", 1.0, 0.3),
        ("Highly elliptic", 1.0, 0.7),
    ]
    
    print(f"\n{'Orbit Type':<20} {'a':<8} {'e':<8} {'Energy':<15} {'Ang. Mom.':<15}")
    print("-" * 70)
    
    for name, a, e in orbits:
        energy = OrbitalMechanics.specific_orbital_energy(a, mu)
        h = OrbitalMechanics.specific_angular_momentum(a, e, mu)
        print(f"{name:<20} {a:<8.2f} {e:<8.2f} {energy:<15.6f} {h:<15.6f}")
    
    print("\n")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("ELLIPTIC CURVES IN CELESTIAL MECHANICS - EXAMPLES")
    print("=" * 70)
    
    example_planetary_orbits()
    example_comet_orbit()
    example_orbital_period()
    example_keplers_equation()
    example_algebraic_curves()
    example_elliptic_integrals()
    example_orbital_velocity()
    example_orbital_energy()
    
    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
