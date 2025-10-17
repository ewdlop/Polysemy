"""
Elliptic Curve Cryptography in the Divine Realm

This module implements elliptic curve cryptography concepts inspired by
the mathematical beauty of "The Da Vinci Code". It integrates the Golden
Ratio (Phi) with elliptic curve operations, creating a bridge between
ancient mathematical proportions and modern cryptography.

The module demonstrates:
1. Elliptic curve point operations
2. Scalar multiplication on elliptic curves
3. Key generation using divine proportions (Phi)
4. Cryptographic primitives based on elliptic curves

An elliptic curve over a field is defined by the equation:
y² = x³ + ax + b

where 4a³ + 27b² ≠ 0 (to ensure the curve is non-singular)
"""

import da_vinci_code


class EllipticCurvePoint:
    """
    Represents a point on an elliptic curve.
    
    The point at infinity is represented by x=None, y=None.
    """
    
    def __init__(self, x, y, curve):
        """
        Initialize a point on an elliptic curve.
        
        Args:
            x: x-coordinate (None for point at infinity)
            y: y-coordinate (None for point at infinity)
            curve: The EllipticCurve this point belongs to
        """
        self.x = x
        self.y = y
        self.curve = curve
        
        if not self.is_at_infinity():
            if not self.curve.is_on_curve(x, y):
                raise ValueError(f"Point ({x}, {y}) is not on the curve")
    
    def is_at_infinity(self):
        """Check if this is the point at infinity (identity element)"""
        return self.x is None and self.y is None
    
    def __eq__(self, other):
        """Check if two points are equal"""
        if not isinstance(other, EllipticCurvePoint):
            return False
        return self.x == other.x and self.y == other.y and self.curve == other.curve
    
    def __add__(self, other):
        """
        Add two points on the elliptic curve.
        
        This implements the elliptic curve group operation.
        """
        if not isinstance(other, EllipticCurvePoint):
            raise TypeError("Can only add EllipticCurvePoint instances")
        
        if self.curve != other.curve:
            raise ValueError("Points must be on the same curve")
        
        # P + O = P
        if self.is_at_infinity():
            return other
        
        # O + Q = Q
        if other.is_at_infinity():
            return self
        
        # P + (-P) = O
        if self.x == other.x and self.y == -other.y % self.curve.p:
            return EllipticCurvePoint(None, None, self.curve)
        
        # Point doubling: P + P
        if self == other:
            # Slope = (3x² + a) / 2y
            numerator = (3 * self.x * self.x + self.curve.a) % self.curve.p
            denominator = (2 * self.y) % self.curve.p
            slope = (numerator * self._mod_inverse(denominator, self.curve.p)) % self.curve.p
        else:
            # Point addition: P + Q
            # Slope = (y₂ - y₁) / (x₂ - x₁)
            numerator = (other.y - self.y) % self.curve.p
            denominator = (other.x - self.x) % self.curve.p
            slope = (numerator * self._mod_inverse(denominator, self.curve.p)) % self.curve.p
        
        # x₃ = slope² - x₁ - x₂
        x3 = (slope * slope - self.x - other.x) % self.curve.p
        # y₃ = slope(x₁ - x₃) - y₁
        y3 = (slope * (self.x - x3) - self.y) % self.curve.p
        
        return EllipticCurvePoint(x3, y3, self.curve)
    
    def __mul__(self, scalar):
        """
        Scalar multiplication: multiply a point by an integer.
        
        This uses the double-and-add algorithm for efficiency.
        """
        if not isinstance(scalar, int):
            raise TypeError("Scalar must be an integer")
        
        if scalar < 0:
            raise ValueError("Scalar must be non-negative")
        
        if scalar == 0:
            return EllipticCurvePoint(None, None, self.curve)
        
        result = EllipticCurvePoint(None, None, self.curve)  # Point at infinity
        addend = self
        
        while scalar:
            if scalar & 1:
                result = result + addend
            addend = addend + addend
            scalar >>= 1
        
        return result
    
    def __rmul__(self, scalar):
        """Support scalar * point notation"""
        return self.__mul__(scalar)
    
    def _mod_inverse(self, a, m):
        """
        Compute modular multiplicative inverse using Extended Euclidean Algorithm.
        
        Returns x such that (a * x) % m == 1
        """
        if a < 0:
            a = (a % m + m) % m
        
        g, x, _ = self._extended_gcd(a, m)
        
        if g != 1:
            raise ValueError(
                f"Modular inverse does not exist for {a} mod {m}. "
                f"This occurs when {a} and {m} are not coprime (gcd = {g})"
            )
        
        return x % m
    
    def _extended_gcd(self, a, b):
        """
        Extended Euclidean Algorithm.
        
        Returns (gcd, x, y) such that a*x + b*y = gcd
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    def __repr__(self):
        """String representation of the point"""
        if self.is_at_infinity():
            return "EllipticCurvePoint(O)"
        return f"EllipticCurvePoint({self.x}, {self.y})"


class EllipticCurve:
    """
    Represents an elliptic curve over a finite field.
    
    The curve is defined by: y² = x³ + ax + b (mod p)
    """
    
    def __init__(self, a, b, p):
        """
        Initialize an elliptic curve.
        
        Args:
            a: Coefficient a in the curve equation
            b: Coefficient b in the curve equation
            p: Prime modulus defining the finite field
        """
        self.a = a
        self.b = b
        self.p = p
        
        # Verify the curve is non-singular
        discriminant = (4 * a**3 + 27 * b**2) % p
        if discriminant == 0:
            raise ValueError("Curve is singular (discriminant is zero)")
    
    def is_on_curve(self, x, y):
        """
        Check if a point (x, y) is on the elliptic curve.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            bool: True if the point is on the curve
        """
        left_side = (y * y) % self.p
        right_side = (x**3 + self.a * x + self.b) % self.p
        return left_side == right_side
    
    def __eq__(self, other):
        """Check if two curves are equal"""
        if not isinstance(other, EllipticCurve):
            return False
        return self.a == other.a and self.b == other.b and self.p == other.p
    
    def __repr__(self):
        """String representation of the curve"""
        return f"EllipticCurve(y² = x³ + {self.a}x + {self.b} mod {self.p})"


# Divine constants derived from the Golden Ratio
DIVINE_PRIME = 163  # A small prime for demonstration, close to Phi * 100


def divine_curve():
    """
    Create the "Divine Curve" inspired by the Golden Ratio.
    
    This curve uses parameters derived from the Golden Ratio (Phi),
    connecting ancient mathematical beauty with modern cryptography.
    
    The divine prime (163) is chosen for its special properties:
    - It's close to 100 * Phi (approximately 161.8)
    - It's a prime number suitable for finite field arithmetic
    - It's small enough for educational/demonstration purposes
    
    Returns:
        EllipticCurve: A curve with divine proportions
    """
    # Calculate Phi with high precision
    phi = da_vinci_code.golden_ratio(100)
    
    # Derive curve parameters from Phi
    # a = floor(Phi) = 1
    a = int(phi)
    
    # b = floor(Phi * 10) mod p
    b = int(phi * 10) % DIVINE_PRIME
    
    return EllipticCurve(a, b, DIVINE_PRIME)


def generate_divine_keypair(curve=None, generator=None, private_key_seed=None):
    """
    Generate a public/private key pair using divine proportions.
    
    The private key is derived from the Fibonacci sequence and Golden Ratio,
    while the public key is computed via elliptic curve scalar multiplication.
    
    Note: This implementation uses predictable sources (Fibonacci and Phi) for
    educational and demonstration purposes. In production cryptographic systems,
    private keys should be generated using cryptographically secure random
    number generators (CSPRNG).
    
    Args:
        curve: The elliptic curve to use (default: divine_curve())
        generator: Generator point on the curve (default: computed)
        private_key_seed: Seed for private key generation (default: from Phi)
        
    Returns:
        tuple: (private_key, public_key) where public_key is an EllipticCurvePoint
    """
    if curve is None:
        curve = divine_curve()
    
    # Generate private key from Fibonacci sequence and Phi
    if private_key_seed is None:
        phi = da_vinci_code.golden_ratio(50)
        fib = da_vinci_code.fibonacci(10)
        # Use Fibonacci numbers and Phi to create a private key
        private_key = int(sum(fib) * phi) % curve.p
        # Ensure private key is not zero
        if private_key == 0:
            private_key = int(phi * 100) % curve.p
    else:
        private_key = private_key_seed % curve.p
    
    # Find a generator point on the curve if not provided
    if generator is None:
        generator = _find_generator_point(curve)
    
    # Compute public key: public_key = private_key * generator
    public_key = generator * private_key
    
    return private_key, public_key


def _find_generator_point(curve):
    """
    Find a valid generator point on the elliptic curve.
    
    Args:
        curve: The elliptic curve
        
    Returns:
        EllipticCurvePoint: A point on the curve
    """
    # Try to find a point on the curve by testing x values
    for x in range(curve.p):
        # Calculate y² = x³ + ax + b
        y_squared = (x**3 + curve.a * x + curve.b) % curve.p
        
        # Check if y_squared is a quadratic residue (has a square root)
        y = _tonelli_shanks(y_squared, curve.p)
        if y is not None:
            # Verify the point is on the curve
            if curve.is_on_curve(x, y):
                return EllipticCurvePoint(x, y, curve)
    
    raise ValueError("Could not find a generator point on the curve")


def _tonelli_shanks(n, p):
    """
    Tonelli-Shanks algorithm to find square root modulo prime.
    
    Args:
        n: Number to find square root of
        p: Prime modulus
        
    Returns:
        int or None: Square root if it exists, None otherwise
    """
    # Check if n is a quadratic residue using Euler's criterion
    if pow(n, (p - 1) // 2, p) != 1:
        return None
    
    # Simple case: p ≡ 3 (mod 4)
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    
    # General case: use Tonelli-Shanks algorithm
    # Find Q and S such that p - 1 = Q * 2^S
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    
    # Find a quadratic non-residue z
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    
    # Initialize variables
    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)
    
    while True:
        if t == 0:
            return 0
        if t == 1:
            return R
        
        # Find the least i such that t^(2^i) = 1
        i = 1
        temp = (t * t) % p
        while temp != 1 and i < M:
            temp = (temp * temp) % p
            i += 1
        
        # Update variables
        b = pow(c, 1 << (M - i - 1), p)
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p


def divine_encrypt(message, public_key, generator):
    """
    Encrypt a message using elliptic curve cryptography.
    
    This implements a simplified ElGamal-style encryption on elliptic curves.
    
    Note: This implementation uses predictable ephemeral keys (from Fibonacci
    and Phi) for demonstration purposes. In production systems, ephemeral keys
    should be generated using cryptographically secure random number generators
    to ensure semantic security (same message encrypted twice produces different
    ciphertexts).
    
    Args:
        message: Integer message to encrypt (must be < curve.p)
        public_key: Recipient's public key (EllipticCurvePoint)
        generator: Generator point
        
    Returns:
        tuple: (C1, C2) where C1 and C2 are EllipticCurvePoints
    """
    # Generate ephemeral private key from Fibonacci
    # WARNING: This is deterministic and for demonstration only!
    phi = da_vinci_code.golden_ratio(30)
    fib = da_vinci_code.fibonacci(8)
    k = int(sum(fib) * phi) % public_key.curve.p
    if k == 0:
        k = int(phi * 50) % public_key.curve.p
    
    # C1 = k * G
    C1 = generator * k
    
    # C2 = M * G + k * public_key
    # For simplicity, encode message as x-coordinate scaling
    M_point = generator * message
    shared_secret = public_key * k
    C2 = M_point + shared_secret
    
    return C1, C2


def divine_decrypt(C1, C2, private_key):
    """
    Decrypt a message using elliptic curve cryptography.
    
    Args:
        C1: First part of ciphertext (EllipticCurvePoint)
        C2: Second part of ciphertext (EllipticCurvePoint)
        private_key: Recipient's private key (integer)
        
    Returns:
        EllipticCurvePoint: Decrypted message point
    """
    # Compute shared_secret = private_key * C1
    shared_secret = C1 * private_key
    
    # M_point = C2 - shared_secret
    # To subtract, we add the negation
    negated_secret = EllipticCurvePoint(
        shared_secret.x,
        -shared_secret.y % shared_secret.curve.p,
        shared_secret.curve
    )
    
    M_point = C2 + negated_secret
    
    return M_point


if __name__ == "__main__":
    print("=" * 70)
    print("ELLIPTIC CURVE CRYPTOGRAPHY IN THE DIVINE REALM")
    print("=" * 70)
    print()
    
    # Display the Golden Ratio connection
    phi = da_vinci_code.golden_ratio(50)
    print(f"The Golden Ratio (Phi): {phi:.15f}")
    print("Phi represents divine proportion in mathematics and nature.")
    print()
    
    # Create the divine curve
    print("Creating the Divine Curve (inspired by Phi)...")
    curve = divine_curve()
    print(f"Curve: {curve}")
    print()
    
    # Find a generator point
    print("Finding a generator point on the curve...")
    generator = _find_generator_point(curve)
    print(f"Generator: {generator}")
    print()
    
    # Generate keypair
    print("Generating cryptographic keys using divine proportions...")
    private_key, public_key = generate_divine_keypair(curve, generator)
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")
    print()
    
    # Demonstrate encryption/decryption
    print("Demonstrating Elliptic Curve Cryptography:")
    message = 42  # Secret message
    print(f"Original message: {message}")
    
    C1, C2 = divine_encrypt(message, public_key, generator)
    print(f"Encrypted: C1 = {C1}, C2 = {C2}")
    
    decrypted = divine_decrypt(C1, C2, private_key)
    print(f"Decrypted point: {decrypted}")
    print()
    
    # Demonstrate point operations
    print("Demonstrating Elliptic Curve Point Operations:")
    P = generator
    print(f"P = {P}")
    
    P2 = P + P
    print(f"2P = P + P = {P2}")
    
    P3 = P2 + P
    print(f"3P = 2P + P = {P3}")
    
    P3_scalar = P * 3
    print(f"3P (via scalar multiplication) = {P3_scalar}")
    print(f"Verification: 3P == 3P? {P3 == P3_scalar}")
    print()
    
    print("=" * 70)
    print("\"The geometry of the elliptic curve reflects divine harmony...\"")
    print("                                    - Cryptographic Wisdom")
    print("=" * 70)
