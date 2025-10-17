"""
Elliptic (Algebraic) Curve in Celestial Mechanics

This module implements elliptic curves and their applications in celestial mechanics,
including:
1. Elliptic orbits (Kepler's laws)
2. Elliptic integrals for orbital calculations
3. Algebraic curve representations for orbital paths
"""

import numpy as np
from typing import Tuple, Optional
import matplotlib.pyplot as plt


class EllipticOrbit:
    """
    Represents an elliptic orbit in celestial mechanics.
    
    An elliptic orbit is described by the equation:
    r = a(1 - e²) / (1 + e*cos(θ))
    
    where:
    - r is the radial distance
    - a is the semi-major axis
    - e is the eccentricity (0 ≤ e < 1 for elliptic orbits)
    - θ is the true anomaly
    """
    
    def __init__(self, semi_major_axis: float, eccentricity: float):
        """
        Initialize an elliptic orbit.
        
        Args:
            semi_major_axis: Semi-major axis of the ellipse (a)
            eccentricity: Eccentricity of the orbit (e), must be 0 ≤ e < 1
        
        Raises:
            ValueError: If eccentricity is not in valid range
        """
        if not 0 <= eccentricity < 1:
            raise ValueError("Eccentricity must be 0 ≤ e < 1 for elliptic orbits")
        
        self.a = semi_major_axis
        self.e = eccentricity
        self.b = semi_major_axis * np.sqrt(1 - eccentricity**2)  # Semi-minor axis
        self.c = semi_major_axis * eccentricity  # Linear eccentricity
    
    def radial_distance(self, true_anomaly: float) -> float:
        """
        Calculate radial distance at a given true anomaly.
        
        Args:
            true_anomaly: Angle θ from periapsis (in radians)
        
        Returns:
            Radial distance r
        """
        return self.a * (1 - self.e**2) / (1 + self.e * np.cos(true_anomaly))
    
    def cartesian_coordinates(self, true_anomaly: float) -> Tuple[float, float]:
        """
        Convert orbital position to Cartesian coordinates.
        
        Args:
            true_anomaly: Angle θ from periapsis (in radians)
        
        Returns:
            Tuple of (x, y) coordinates
        """
        r = self.radial_distance(true_anomaly)
        x = r * np.cos(true_anomaly)
        y = r * np.sin(true_anomaly)
        return x, y
    
    def periapsis(self) -> float:
        """Return the periapsis distance (closest approach)."""
        return self.a * (1 - self.e)
    
    def apoapsis(self) -> float:
        """Return the apoapsis distance (farthest point)."""
        return self.a * (1 + self.e)
    
    def orbital_period(self, mu: float) -> float:
        """
        Calculate orbital period using Kepler's third law.
        
        Args:
            mu: Standard gravitational parameter (G*M)
        
        Returns:
            Orbital period T
        """
        return 2 * np.pi * np.sqrt(self.a**3 / mu)
    
    def mean_motion(self, mu: float) -> float:
        """
        Calculate mean motion n = 2π/T.
        
        Args:
            mu: Standard gravitational parameter (G*M)
        
        Returns:
            Mean motion n
        """
        return np.sqrt(mu / self.a**3)
    
    def eccentric_anomaly_from_mean(self, mean_anomaly: float, tolerance: float = 1e-10) -> float:
        """
        Solve Kepler's equation M = E - e*sin(E) for eccentric anomaly E.
        Uses Newton-Raphson iteration.
        
        Args:
            mean_anomaly: Mean anomaly M (in radians)
            tolerance: Convergence tolerance
        
        Returns:
            Eccentric anomaly E
        """
        # Initial guess
        E = mean_anomaly if self.e < 0.8 else np.pi
        
        # Newton-Raphson iteration
        max_iterations = 100
        for _ in range(max_iterations):
            f = E - self.e * np.sin(E) - mean_anomaly
            f_prime = 1 - self.e * np.cos(E)
            E_new = E - f / f_prime
            
            if abs(E_new - E) < tolerance:
                return E_new
            E = E_new
        
        return E
    
    def true_anomaly_from_eccentric(self, eccentric_anomaly: float) -> float:
        """
        Convert eccentric anomaly to true anomaly.
        
        Args:
            eccentric_anomaly: Eccentric anomaly E (in radians)
        
        Returns:
            True anomaly θ
        """
        return 2 * np.arctan2(
            np.sqrt(1 + self.e) * np.sin(eccentric_anomaly / 2),
            np.sqrt(1 - self.e) * np.cos(eccentric_anomaly / 2)
        )
    
    def plot_orbit(self, num_points: int = 1000) -> None:
        """
        Plot the elliptic orbit.
        
        Args:
            num_points: Number of points to plot
        """
        theta = np.linspace(0, 2*np.pi, num_points)
        x = np.array([self.cartesian_coordinates(t)[0] for t in theta])
        y = np.array([self.cartesian_coordinates(t)[1] for t in theta])
        
        plt.figure(figsize=(10, 8))
        plt.plot(x, y, 'b-', linewidth=2, label='Orbit')
        plt.plot(0, 0, 'yo', markersize=15, label='Central Body')
        plt.plot(self.periapsis(), 0, 'ro', markersize=8, label='Periapsis')
        plt.plot(-self.apoapsis(), 0, 'go', markersize=8, label='Apoapsis')
        
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Elliptic Orbit (a={self.a}, e={self.e})')
        plt.axis('equal')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()


class AlgebraicCurve:
    """
    Represents an algebraic curve in the form of a conic section.
    
    General equation: Ax² + Bxy + Cy² + Dx + Ey + F = 0
    """
    
    def __init__(self, A: float, B: float, C: float, D: float, E: float, F: float):
        """
        Initialize an algebraic curve.
        
        Args:
            A, B, C, D, E, F: Coefficients of the general conic equation
        """
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E
        self.F = F
    
    def discriminant(self) -> float:
        """
        Calculate the discriminant B² - 4AC.
        
        Returns:
            Discriminant value
            - < 0: Ellipse
            - = 0: Parabola
            - > 0: Hyperbola
        """
        return self.B**2 - 4*self.A*self.C
    
    def curve_type(self) -> str:
        """
        Determine the type of conic section.
        
        Returns:
            String describing the curve type
        """
        disc = self.discriminant()
        if disc < 0:
            return "Ellipse"
        elif disc == 0:
            return "Parabola"
        else:
            return "Hyperbola"
    
    @staticmethod
    def from_ellipse(a: float, b: float, center: Tuple[float, float] = (0, 0)) -> 'AlgebraicCurve':
        """
        Create an algebraic curve from ellipse parameters.
        
        Args:
            a: Semi-major axis
            b: Semi-minor axis
            center: Center coordinates (h, k)
        
        Returns:
            AlgebraicCurve instance representing the ellipse
        """
        h, k = center
        # (x-h)²/a² + (y-k)²/b² = 1
        # Expanding: b²(x-h)² + a²(y-k)² = a²b²
        A = b**2
        B = 0
        C = a**2
        D = -2*b**2*h
        E = -2*a**2*k
        F = b**2*h**2 + a**2*k**2 - a**2*b**2
        
        return AlgebraicCurve(A, B, C, D, E, F)


class EllipticIntegrals:
    """
    Compute elliptic integrals used in celestial mechanics.
    
    Elliptic integrals appear in calculations involving:
    - Arc length of ellipses
    - Time of flight calculations
    - Perturbed orbital motion
    """
    
    @staticmethod
    def complete_elliptic_integral_first_kind(k: float, num_terms: int = 100) -> float:
        """
        Compute complete elliptic integral of the first kind K(k).
        
        K(k) = ∫[0 to π/2] dθ / sqrt(1 - k²sin²θ)
        
        Uses arithmetic-geometric mean (AGM) method for high accuracy.
        
        Args:
            k: Modulus (0 ≤ k < 1)
            num_terms: Number of AGM iterations
        
        Returns:
            Value of K(k)
        """
        if not 0 <= k < 1:
            raise ValueError("Modulus k must satisfy 0 ≤ k < 1")
        
        a = 1.0
        g = np.sqrt(1 - k**2)
        
        for _ in range(num_terms):
            a_new = (a + g) / 2
            g = np.sqrt(a * g)
            a = a_new
            
            if abs(a - g) < 1e-15:
                break
        
        return np.pi / (2 * a)
    
    @staticmethod
    def complete_elliptic_integral_second_kind(k: float, num_terms: int = 100) -> float:
        """
        Compute complete elliptic integral of the second kind E(k).
        
        E(k) = ∫[0 to π/2] sqrt(1 - k²sin²θ) dθ
        
        Args:
            k: Modulus (0 ≤ k < 1)
            num_terms: Number of terms in series
        
        Returns:
            Value of E(k)
        """
        if not 0 <= k < 1:
            raise ValueError("Modulus k must satisfy 0 ≤ k < 1")
        
        # Using series expansion
        E = np.pi / 2
        k2 = k**2
        term = k2 / 4
        
        for n in range(1, num_terms):
            E -= term / (2*n - 1)
            term *= k2 * (2*n - 1)**2 / (2*n * (2*n + 1))
            
            if abs(term) < 1e-15:
                break
        
        return E
    
    @staticmethod
    def ellipse_perimeter(a: float, b: float) -> float:
        """
        Calculate the perimeter of an ellipse using elliptic integrals.
        
        Args:
            a: Semi-major axis
            b: Semi-minor axis
        
        Returns:
            Perimeter of the ellipse
        """
        if a < b:
            a, b = b, a
        
        e = np.sqrt(1 - (b/a)**2)
        E = EllipticIntegrals.complete_elliptic_integral_second_kind(e)
        
        return 4 * a * E


class OrbitalMechanics:
    """
    Utility class for common orbital mechanics calculations.
    """
    
    @staticmethod
    def vis_viva_equation(r: float, a: float, mu: float) -> float:
        """
        Calculate orbital velocity using the vis-viva equation.
        
        v² = μ(2/r - 1/a)
        
        Args:
            r: Current radial distance
            a: Semi-major axis
            mu: Standard gravitational parameter
        
        Returns:
            Orbital velocity
        """
        return np.sqrt(mu * (2/r - 1/a))
    
    @staticmethod
    def specific_orbital_energy(a: float, mu: float) -> float:
        """
        Calculate specific orbital energy.
        
        ε = -μ/(2a)
        
        Args:
            a: Semi-major axis
            mu: Standard gravitational parameter
        
        Returns:
            Specific orbital energy
        """
        return -mu / (2 * a)
    
    @staticmethod
    def specific_angular_momentum(a: float, e: float, mu: float) -> float:
        """
        Calculate specific angular momentum.
        
        h = sqrt(μ * a * (1 - e²))
        
        Args:
            a: Semi-major axis
            e: Eccentricity
            mu: Standard gravitational parameter
        
        Returns:
            Specific angular momentum
        """
        return np.sqrt(mu * a * (1 - e**2))


# Example usage and demonstrations
if __name__ == "__main__":
    print("=" * 60)
    print("Elliptic Curves in Celestial Mechanics")
    print("=" * 60)
    
    # Example 1: Earth-like orbit
    print("\n1. Earth-like Elliptic Orbit:")
    print("-" * 60)
    earth_orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.0167)
    print(f"Semi-major axis: {earth_orbit.a} AU")
    print(f"Eccentricity: {earth_orbit.e}")
    print(f"Semi-minor axis: {earth_orbit.b:.6f} AU")
    print(f"Perihelion: {earth_orbit.periapsis():.6f} AU")
    print(f"Aphelion: {earth_orbit.apoapsis():.6f} AU")
    
    # Example 2: Halley's Comet orbit
    print("\n2. Halley's Comet Elliptic Orbit:")
    print("-" * 60)
    halley_orbit = EllipticOrbit(semi_major_axis=17.8, eccentricity=0.967)
    print(f"Semi-major axis: {halley_orbit.a} AU")
    print(f"Eccentricity: {halley_orbit.e}")
    print(f"Perihelion: {halley_orbit.periapsis():.3f} AU")
    print(f"Aphelion: {halley_orbit.apoapsis():.3f} AU")
    
    # Example 3: Algebraic curve representation
    print("\n3. Algebraic Curve Representation:")
    print("-" * 60)
    curve = AlgebraicCurve.from_ellipse(a=2.0, b=1.5)
    print(f"Curve type: {curve.curve_type()}")
    print(f"Discriminant: {curve.discriminant():.6f}")
    print(f"Coefficients: A={curve.A}, B={curve.B}, C={curve.C}")
    print(f"              D={curve.D}, E={curve.E}, F={curve.F}")
    
    # Example 4: Elliptic integrals
    print("\n4. Elliptic Integrals:")
    print("-" * 60)
    k = 0.5
    K = EllipticIntegrals.complete_elliptic_integral_first_kind(k)
    E = EllipticIntegrals.complete_elliptic_integral_second_kind(k)
    print(f"For modulus k = {k}:")
    print(f"K(k) = {K:.10f}")
    print(f"E(k) = {E:.10f}")
    
    perimeter = EllipticIntegrals.ellipse_perimeter(a=2.0, b=1.5)
    print(f"\nPerimeter of ellipse (a=2.0, b=1.5): {perimeter:.10f}")
    
    # Example 5: Orbital mechanics calculations
    print("\n5. Orbital Mechanics:")
    print("-" * 60)
    mu = 1.0  # Normalized gravitational parameter
    a = 1.0
    e = 0.2
    r = earth_orbit.periapsis()
    
    v = OrbitalMechanics.vis_viva_equation(r, a, mu)
    energy = OrbitalMechanics.specific_orbital_energy(a, mu)
    h = OrbitalMechanics.specific_angular_momentum(a, e, mu)
    
    print(f"At periapsis (r = {r:.6f}):")
    print(f"  Velocity: {v:.6f}")
    print(f"  Specific energy: {energy:.6f}")
    print(f"  Specific angular momentum: {h:.6f}")
    
    # Example 6: Kepler's equation
    print("\n6. Solving Kepler's Equation:")
    print("-" * 60)
    M = np.pi / 4  # Mean anomaly
    E = earth_orbit.eccentric_anomaly_from_mean(M)
    theta = earth_orbit.true_anomaly_from_eccentric(E)
    print(f"Mean anomaly M = {M:.6f} rad ({np.degrees(M):.2f}°)")
    print(f"Eccentric anomaly E = {E:.6f} rad ({np.degrees(E):.2f}°)")
    print(f"True anomaly θ = {theta:.6f} rad ({np.degrees(theta):.2f}°)")
    
    print("\n" + "=" * 60)
    print("Calculations complete!")
    print("=" * 60)
