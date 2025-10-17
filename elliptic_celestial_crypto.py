"""
Elliptic Curve Cryptography in Celestial Mechanics

This module implements Elliptic Curve Cryptography (ECC) with a celestial mechanics theme,
combining cryptographic principles with orbital mechanics.

Elliptic curves in cryptography are defined by the equation:
    y² = x³ + ax + b (mod p)

These curves are analogous to elliptical orbits in celestial mechanics, described by Kepler's laws.
The module demonstrates how mathematical structures used in cryptography mirror those in physics.

Key Concepts:
1. Elliptic Curve Points - Like celestial bodies in orbital positions
2. Point Addition - Similar to gravitational interactions between bodies
3. Scalar Multiplication - Analogous to orbital period calculations
4. Public/Private Key Generation - Inspired by orbital parameters
"""

import hashlib
import secrets
from typing import Tuple, Optional


class EllipticCurve:
    """
    Represents an elliptic curve over a finite field.
    
    The curve equation is: y² = x³ + ax + b (mod p)
    
    This mirrors the mathematical structure of orbital mechanics where
    elliptical paths are fundamental to celestial body motion.
    """
    
    def __init__(self, a: int, b: int, p: int):
        """
        Initialize an elliptic curve with parameters a, b, and prime p.
        
        Args:
            a (int): Coefficient a in the curve equation
            b (int): Coefficient b in the curve equation
            p (int): Prime modulus defining the finite field
            
        Raises:
            ValueError: If the curve is singular (discriminant is zero)
        """
        self.a = a
        self.b = b
        self.p = p
        
        # Check that the curve is non-singular: 4a³ + 27b² ≠ 0 (mod p)
        discriminant = (4 * a**3 + 27 * b**2) % p
        if discriminant == 0:
            raise ValueError("The curve is singular (discriminant is zero)")
    
    def is_on_curve(self, point: Optional[Tuple[int, int]]) -> bool:
        """
        Check if a point lies on the elliptic curve.
        
        Args:
            point: A tuple (x, y) or None (point at infinity)
            
        Returns:
            bool: True if the point is on the curve
        """
        if point is None:  # Point at infinity
            return True
        
        x, y = point
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0
    
    def point_addition(self, P: Optional[Tuple[int, int]], 
                      Q: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """
        Add two points on the elliptic curve.
        
        This operation is analogous to the superposition of gravitational
        influences in celestial mechanics.
        
        Args:
            P: First point (x, y) or None
            Q: Second point (x, y) or None
            
        Returns:
            The sum of P and Q on the curve, or None (point at infinity)
        """
        # Handle point at infinity
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        # Handle case where P = -Q (vertical line)
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None  # Point at infinity
        
        # Calculate slope
        if P == Q:
            # Point doubling (tangent line)
            # slope = (3x₁² + a) / (2y₁)
            slope = (3 * x1**2 + self.a) * pow(2 * y1, -1, self.p)
        else:
            # Two distinct points (secant line)
            # slope = (y₂ - y₁) / (x₂ - x₁)
            slope = (y2 - y1) * pow(x2 - x1, -1, self.p)
        
        slope %= self.p
        
        # Calculate the new point
        x3 = (slope**2 - x1 - x2) % self.p
        y3 = (slope * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def scalar_multiplication(self, k: int, 
                             P: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """
        Multiply a point P by a scalar k using the double-and-add algorithm.
        
        This is analogous to calculating orbital positions after k periods
        in celestial mechanics.
        
        Args:
            k: Scalar multiplier (like number of orbital periods)
            P: Point to multiply (like initial orbital position)
            
        Returns:
            The result of k*P on the curve
        """
        if k == 0 or P is None:
            return None  # Point at infinity
        
        if k < 0:
            # Negate the point and make k positive
            k = -k
            P = (P[0], -P[1] % self.p)
        
        # Double-and-add algorithm
        result = None
        addend = P
        
        while k:
            if k & 1:  # If bit is set
                result = self.point_addition(result, addend)
            addend = self.point_addition(addend, addend)
            k >>= 1
        
        return result
    
    def __repr__(self):
        return f"EllipticCurve(a={self.a}, b={self.b}, p={self.p})"


class OrbitalCryptoSystem:
    """
    A cryptographic system based on elliptic curves with orbital mechanics theme.
    
    Uses the secp256k1 curve (same as Bitcoin) as the "gravitational field"
    for our celestial cryptographic system.
    """
    
    # secp256k1 parameters (used in Bitcoin)
    # These parameters define a "gravitational field" for our cryptographic orbits
    P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    A = 0
    B = 7
    # Generator point (base point) - like the Sun in a solar system
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    # Order of the generator point
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    
    def __init__(self):
        """Initialize the orbital cryptographic system with secp256k1 parameters."""
        self.curve = EllipticCurve(self.A, self.B, self.P)
        self.G = (self.Gx, self.Gy)  # Generator point (the "Sun")
    
    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """
        Generate a public/private key pair.
        
        The private key is like a secret orbital parameter, and the public key
        is the observable position of a celestial body.
        
        Returns:
            A tuple (private_key, public_key) where:
                - private_key: A random integer (secret orbital parameter)
                - public_key: A point on the curve (observable position)
        """
        # Generate a random private key (1 to N-1)
        private_key = secrets.randbelow(self.N - 1) + 1
        
        # Calculate public key = private_key * G
        # Like calculating orbital position from initial conditions
        public_key = self.curve.scalar_multiplication(private_key, self.G)
        
        return private_key, public_key
    
    def compute_shared_secret(self, private_key: int, 
                             other_public_key: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Compute a shared secret using Elliptic Curve Diffie-Hellman (ECDH).
        
        This is analogous to two celestial bodies finding a common orbital resonance.
        
        Args:
            private_key: Your private key (secret orbital parameter)
            other_public_key: Other party's public key (their orbital position)
            
        Returns:
            A shared point that both parties can compute independently
        """
        return self.curve.scalar_multiplication(private_key, other_public_key)
    
    def orbital_signature(self, message: str, private_key: int) -> Tuple[int, int]:
        """
        Create a simple signature using the private key.
        
        This demonstrates how orbital parameters can "sign" a message,
        like how planetary positions can mark specific times.
        
        Args:
            message: The message to sign
            private_key: The private key (secret orbital parameter)
            
        Returns:
            A signature tuple (r, s)
        """
        # Hash the message to get a fixed-size value
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % self.N
        
        # Generate a random k (like a random orbital phase)
        k = secrets.randbelow(self.N - 1) + 1
        
        # Calculate point R = k * G
        R = self.curve.scalar_multiplication(k, self.G)
        if R is None:
            raise ValueError("Invalid signature generation")
        
        r = R[0] % self.N
        if r == 0:
            raise ValueError("Invalid signature (r is zero)")
        
        # Calculate s = k^(-1) * (h + r * private_key) mod N
        k_inv = pow(k, -1, self.N)
        s = (k_inv * (h + r * private_key)) % self.N
        
        if s == 0:
            raise ValueError("Invalid signature (s is zero)")
        
        return (r, s)
    
    def verify_signature(self, message: str, signature: Tuple[int, int], 
                        public_key: Tuple[int, int]) -> bool:
        """
        Verify a signature using the public key.
        
        This is like verifying that a celestial body is in the expected position
        based on known orbital mechanics.
        
        Args:
            message: The original message
            signature: The signature tuple (r, s)
            public_key: The public key (orbital position)
            
        Returns:
            True if the signature is valid, False otherwise
        """
        r, s = signature
        
        # Verify r and s are in the valid range
        if not (1 <= r < self.N and 1 <= s < self.N):
            return False
        
        # Hash the message
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % self.N
        
        # Calculate verification values
        s_inv = pow(s, -1, self.N)
        u1 = (h * s_inv) % self.N
        u2 = (r * s_inv) % self.N
        
        # Calculate point P = u1 * G + u2 * public_key
        point1 = self.curve.scalar_multiplication(u1, self.G)
        point2 = self.curve.scalar_multiplication(u2, public_key)
        P = self.curve.point_addition(point1, point2)
        
        if P is None:
            return False
        
        # Verify that r matches the x-coordinate of P
        return r == P[0] % self.N


def kepler_orbital_analogy():
    """
    Demonstrate the analogy between elliptic curve operations and Kepler's laws.
    
    This is an educational function showing the conceptual connection between
    cryptographic elliptic curves and celestial mechanics.
    """
    print("=" * 70)
    print("ELLIPTIC CURVE CRYPTOGRAPHY IN CELESTIAL MECHANICS")
    print("=" * 70)
    print()
    
    print("The Mathematical Bridge Between Cryptography and Orbital Mechanics:")
    print()
    print("1. ELLIPTIC CURVES (Cryptography)  ↔  ELLIPTICAL ORBITS (Kepler)")
    print("   y² = x³ + ax + b (mod p)        ↔  r = a(1-e²)/(1+e·cosθ)")
    print()
    print("2. POINT ADDITION (ECC)            ↔  GRAVITATIONAL INTERACTION")
    print("   Combining curve points          ↔  Superposition of forces")
    print()
    print("3. SCALAR MULTIPLICATION (ECC)     ↔  ORBITAL PERIOD CALCULATION")
    print("   k·P = P + P + ... + P           ↔  Position after k periods")
    print()
    print("4. GENERATOR POINT G               ↔  THE SUN (Central body)")
    print("   Base point for all operations   ↔  Center of orbital system")
    print()
    print("5. PRIVATE KEY                     ↔  ORBITAL PARAMETERS (secret)")
    print("   Secret scalar                   ↔  Exact initial conditions")
    print()
    print("6. PUBLIC KEY                      ↔  OBSERVABLE POSITION")
    print("   k·G on the curve                ↔  Visible celestial position")
    print()
    print("=" * 70)


if __name__ == "__main__":
    # Display the analogy
    kepler_orbital_analogy()
    print()
    
    # Initialize the orbital cryptographic system
    print("Initializing Orbital Cryptographic System (secp256k1)...")
    crypto_system = OrbitalCryptoSystem()
    print(f"Curve: {crypto_system.curve}")
    print(f"Generator Point (The Sun): G = ({hex(crypto_system.Gx)[:20]}..., {hex(crypto_system.Gy)[:20]}...)")
    print()
    
    # Demonstrate key generation
    print("=" * 70)
    print("ORBITAL KEY GENERATION (Celestial Positions)")
    print("=" * 70)
    
    # Alice generates her keys
    alice_private, alice_public = crypto_system.generate_keypair()
    print(f"Alice's Orbital Parameters (Private Key): {hex(alice_private)[:40]}...")
    print(f"Alice's Observable Position (Public Key):")
    print(f"  x = {hex(alice_public[0])[:40]}...")
    print(f"  y = {hex(alice_public[1])[:40]}...")
    print()
    
    # Bob generates his keys
    bob_private, bob_public = crypto_system.generate_keypair()
    print(f"Bob's Orbital Parameters (Private Key): {hex(bob_private)[:40]}...")
    print(f"Bob's Observable Position (Public Key):")
    print(f"  x = {hex(bob_public[0])[:40]}...")
    print(f"  y = {hex(bob_public[1])[:40]}...")
    print()
    
    # Demonstrate ECDH (shared secret)
    print("=" * 70)
    print("ORBITAL RESONANCE (Shared Secret via ECDH)")
    print("=" * 70)
    
    alice_shared = crypto_system.compute_shared_secret(alice_private, bob_public)
    bob_shared = crypto_system.compute_shared_secret(bob_private, alice_public)
    
    print("Alice computes: alice_private · bob_public")
    print("Bob computes: bob_private · alice_public")
    print()
    
    if alice_shared == bob_shared:
        print("✓ Orbital resonance achieved! Both parties computed the same point:")
        print(f"  Shared Secret x = {hex(alice_shared[0])[:40]}...")
        print(f"  Shared Secret y = {hex(alice_shared[1])[:40]}...")
    else:
        print("✗ Orbital resonance failed (this should never happen)")
    print()
    
    # Demonstrate digital signatures
    print("=" * 70)
    print("ORBITAL SIGNATURE (Cryptographic Authentication)")
    print("=" * 70)
    
    message = "The celestial dance reveals the hidden truth"
    print(f"Message: '{message}'")
    print()
    
    # Alice signs the message
    signature = crypto_system.orbital_signature(message, alice_private)
    print(f"Alice's Orbital Signature:")
    print(f"  r = {hex(signature[0])[:40]}...")
    print(f"  s = {hex(signature[1])[:40]}...")
    print()
    
    # Verify with Alice's public key
    is_valid = crypto_system.verify_signature(message, signature, alice_public)
    print(f"Verification with Alice's public key: {is_valid}")
    print()
    
    # Try to verify with wrong public key (should fail)
    is_valid_wrong = crypto_system.verify_signature(message, signature, bob_public)
    print(f"Verification with Bob's public key: {is_valid_wrong}")
    print()
    
    # Try to verify tampered message (should fail)
    tampered_message = "The celestial dance reveals the hidden lies"
    is_valid_tampered = crypto_system.verify_signature(tampered_message, signature, alice_public)
    print(f"Verification of tampered message: {is_valid_tampered}")
    print()
    
    print("=" * 70)
    print("Like planets in predictable orbits, cryptographic operations")
    print("follow the elegant mathematics of elliptic curves.")
    print("=" * 70)
