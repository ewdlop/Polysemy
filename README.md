# Polysemy

改變過去是(心((虛)能))

## Elliptic (Algebraic) Curve in Celestial Mechanics

This repository implements mathematical models for elliptic curves and their applications in celestial mechanics, including elliptic orbits, elliptic integrals, and algebraic curve representations.

### Features

- **Elliptic Orbits**: Complete implementation of Keplerian elliptic orbits
  - Orbital parameters (semi-major axis, eccentricity, periapsis, apoapsis)
  - Position calculations using true anomaly
  - Kepler's equation solver (Mean → Eccentric → True anomaly)
  - Orbital period and mean motion calculations
  - Cartesian coordinate conversions

- **Algebraic Curves**: Representation of conic sections
  - General conic equation: Ax² + Bxy + Cy² + Dx + Ey + F = 0
  - Discriminant analysis for curve type identification
  - Ellipse parameterization from geometric parameters

- **Elliptic Integrals**: Mathematical functions for advanced orbital calculations
  - Complete elliptic integral of the first kind K(k)
  - Complete elliptic integral of the second kind E(k)
  - Ellipse perimeter calculations
  - Applications to orbital arc length and time-of-flight

- **Orbital Mechanics**: Utility functions for orbital dynamics
  - Vis-viva equation for orbital velocity
  - Specific orbital energy
  - Specific angular momentum

### Installation

```bash
# Clone the repository
git clone https://github.com/ewdlop/Polysemy.git
cd Polysemy

# Install required dependencies
pip install numpy matplotlib
```

### Usage

#### Basic Elliptic Orbit

```python
from elliptic_curve_celestial_mechanics import EllipticOrbit

# Create an Earth-like orbit
earth_orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.0167)

print(f"Perihelion: {earth_orbit.periapsis()} AU")
print(f"Aphelion: {earth_orbit.apoapsis()} AU")

# Calculate position at true anomaly θ = π/4
theta = 3.14159 / 4
r = earth_orbit.radial_distance(theta)
x, y = earth_orbit.cartesian_coordinates(theta)
print(f"Position: r={r}, x={x}, y={y}")
```

#### Solving Kepler's Equation

```python
from elliptic_curve_celestial_mechanics import EllipticOrbit
import numpy as np

orbit = EllipticOrbit(semi_major_axis=1.0, eccentricity=0.3)

# Convert mean anomaly to true anomaly
M = np.pi / 4  # Mean anomaly
E = orbit.eccentric_anomaly_from_mean(M)
theta = orbit.true_anomaly_from_eccentric(E)

print(f"Mean anomaly: {M}")
print(f"Eccentric anomaly: {E}")
print(f"True anomaly: {theta}")
```

#### Algebraic Curves

```python
from elliptic_curve_celestial_mechanics import AlgebraicCurve

# Create an ellipse from geometric parameters
curve = AlgebraicCurve.from_ellipse(a=2.0, b=1.5)

print(f"Curve type: {curve.curve_type()}")
print(f"Discriminant: {curve.discriminant()}")
```

#### Elliptic Integrals

```python
from elliptic_curve_celestial_mechanics import EllipticIntegrals

# Calculate complete elliptic integrals
k = 0.5
K = EllipticIntegrals.complete_elliptic_integral_first_kind(k)
E = EllipticIntegrals.complete_elliptic_integral_second_kind(k)

print(f"K({k}) = {K}")
print(f"E({k}) = {E}")

# Calculate ellipse perimeter
perimeter = EllipticIntegrals.ellipse_perimeter(a=2.0, b=1.5)
print(f"Ellipse perimeter: {perimeter}")
```

#### Orbital Mechanics

```python
from elliptic_curve_celestial_mechanics import OrbitalMechanics

mu = 1.0  # Gravitational parameter
a = 1.0   # Semi-major axis
e = 0.2   # Eccentricity
r = 0.8   # Current distance

# Calculate orbital velocity
v = OrbitalMechanics.vis_viva_equation(r, a, mu)
print(f"Orbital velocity: {v}")

# Calculate specific energy and angular momentum
energy = OrbitalMechanics.specific_orbital_energy(a, mu)
h = OrbitalMechanics.specific_angular_momentum(a, e, mu)
print(f"Specific energy: {energy}")
print(f"Angular momentum: {h}")
```

### Examples

Run the comprehensive examples file to see all features in action:

```bash
python examples.py
```

This will demonstrate:
- Real planetary orbits (Mercury through Saturn)
- Halley's Comet highly eccentric orbit
- Orbital period calculations
- Kepler's equation solving
- Algebraic curve representations
- Elliptic integral computations
- Orbital velocity calculations
- Energy and angular momentum

### Running the Main Module

```bash
python elliptic_curve_celestial_mechanics.py
```

This will run built-in demonstrations of all the core functionality.

### Mathematical Background

#### Elliptic Orbits

An elliptic orbit is described by the polar equation:

```
r = a(1 - e²) / (1 + e·cos(θ))
```

where:
- `r` is the radial distance
- `a` is the semi-major axis
- `e` is the eccentricity (0 ≤ e < 1)
- `θ` is the true anomaly

#### Kepler's Equation

The relationship between mean anomaly (M), eccentric anomaly (E), and eccentricity (e):

```
M = E - e·sin(E)
```

This is solved iteratively using Newton-Raphson method.

#### Elliptic Integrals

Complete elliptic integral of the first kind:
```
K(k) = ∫[0 to π/2] dθ / √(1 - k²sin²θ)
```

Complete elliptic integral of the second kind:
```
E(k) = ∫[0 to π/2] √(1 - k²sin²θ) dθ
```

These integrals are essential for calculating arc lengths and periods in elliptic motion.

### License

This project is open source and available for educational and research purposes.

### Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
