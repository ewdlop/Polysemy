# Quick Reference Guide: Elliptic Curves in Celestial Mechanics

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from elliptic_curve_celestial_mechanics import EllipticOrbit
import numpy as np

# Create an orbit
orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.2)

# Get orbital parameters
print(f"Perihelion: {orbit.periapsis()} AU")
print(f"Aphelion: {orbit.apoapsis()} AU")

# Calculate position at true anomaly θ = 45°
theta = np.radians(45)
r = orbit.radial_distance(theta)
x, y = orbit.cartesian_coordinates(theta)
```

## Common Use Cases

### 1. Planetary Orbits

```python
# Earth's orbit
earth = EllipticOrbit(1.0, 0.0167)
print(earth.periapsis())  # 0.9833 AU
```

### 2. Kepler's Equation

```python
# Convert mean anomaly to true anomaly
M = np.pi / 4  # Mean anomaly
E = orbit.eccentric_anomaly_from_mean(M)  # Eccentric anomaly
theta = orbit.true_anomaly_from_eccentric(E)  # True anomaly
```

### 3. Elliptic Integrals

```python
from elliptic_curve_celestial_mechanics import EllipticIntegrals

# Complete elliptic integrals
K = EllipticIntegrals.complete_elliptic_integral_first_kind(0.5)
E = EllipticIntegrals.complete_elliptic_integral_second_kind(0.5)

# Ellipse perimeter
perimeter = EllipticIntegrals.ellipse_perimeter(2.0, 1.5)
```

### 4. Orbital Velocity

```python
from elliptic_curve_celestial_mechanics import OrbitalMechanics

mu = 1.0  # Gravitational parameter
a = 1.0   # Semi-major axis
r = 0.8   # Current distance

v = OrbitalMechanics.vis_visa_equation(r, a, mu)
```

### 5. Algebraic Curves

```python
from elliptic_curve_celestial_mechanics import AlgebraicCurve

curve = AlgebraicCurve.from_ellipse(a=2.0, b=1.5)
print(curve.curve_type())  # "Ellipse"
print(curve.discriminant())  # < 0 for ellipse
```

## Running Examples

```bash
# Run comprehensive examples
python examples.py

# Run main module demonstrations
python elliptic_curve_celestial_mechanics.py

# Run tests
python test_elliptic_curve.py
```

## Key Formulas

### Orbit Equation
```
r = a(1 - e²) / (1 + e·cos(θ))
```

### Kepler's Equation
```
M = E - e·sin(E)
```

### Vis-Viva Equation
```
v² = μ(2/r - 1/a)
```

### Orbital Period
```
T = 2π√(a³/μ)
```

## Parameters

- `a` - Semi-major axis
- `e` - Eccentricity (0 ≤ e < 1 for ellipse)
- `r` - Radial distance
- `θ` - True anomaly
- `M` - Mean anomaly
- `E` - Eccentric anomaly
- `μ` - Standard gravitational parameter (G·M)
- `v` - Orbital velocity

## Classes

### EllipticOrbit
- `radial_distance(theta)` - Distance at angle θ
- `cartesian_coordinates(theta)` - (x, y) position
- `periapsis()` - Closest approach
- `apoapsis()` - Farthest point
- `orbital_period(mu)` - Period T
- `eccentric_anomaly_from_mean(M)` - Solve Kepler's equation
- `true_anomaly_from_eccentric(E)` - Convert E to θ

### AlgebraicCurve
- `curve_type()` - "Ellipse", "Parabola", or "Hyperbola"
- `discriminant()` - B² - 4AC
- `from_ellipse(a, b)` - Create from ellipse parameters

### EllipticIntegrals
- `complete_elliptic_integral_first_kind(k)` - K(k)
- `complete_elliptic_integral_second_kind(k)` - E(k)
- `ellipse_perimeter(a, b)` - Exact perimeter

### OrbitalMechanics
- `vis_viva_equation(r, a, mu)` - Velocity at distance r
- `specific_orbital_energy(a, mu)` - ε = -μ/(2a)
- `specific_angular_momentum(a, e, mu)` - h = √(μa(1-e²))

## Real-World Examples

### Mercury
```python
mercury = EllipticOrbit(0.387, 0.206)
```

### Earth
```python
earth = EllipticOrbit(1.0, 0.017)
```

### Mars
```python
mars = EllipticOrbit(1.524, 0.093)
```

### Halley's Comet
```python
halley = EllipticOrbit(17.8, 0.967)
```

## Tips

- For circular orbits, set `e = 0`
- All angles are in radians
- Distance units are arbitrary but must be consistent
- For solar system, use AU and years for natural units
- Eccentricity must be 0 ≤ e < 1 for elliptic orbits
